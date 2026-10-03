"""Agente nativo Windows. Autenticado; não aceita comandos arbitrários."""

import argparse
import hmac
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from quickmapgo.core import Controller, Coordinate, DemoGateway, GatewayError
from quickmapgo.device import PmdGateway


def make_server(address, controller, token):
    if len(token) < 32:
        raise ValueError("QUICKMAPGO_AGENT_TOKEN deve conter pelo menos 32 caracteres.")

    class Handler(BaseHTTPRequestHandler):
        def setup(self):
            super().setup()
            self.connection.settimeout(5)

        def log_message(self, *_):
            pass  # Não registrar dados do dispositivo nem headers.

        def reply(self, status, payload):
            encoded = json.dumps(payload).encode()
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(encoded)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(encoded)

        def do_POST(self):
            if self.path != "/api":
                return self.reply(404, {"error": "not_found"})
            if not hmac.compare_digest(self.headers.get("Authorization", ""), f"Bearer {token}"):
                return self.reply(401, {"error": "unauthorized"})
            try:
                length = int(self.headers.get("Content-Length", "0"))
                if not 0 < length <= 4096:
                    return self.reply(413, {"error": "invalid_size"})
                body = json.loads(self.rfile.read(length))
                action = body["action"]
                if action == "discover":
                    result = {"devices": controller.gateway.discover(body["transport"])}
                elif action == "connect":
                    controller.connect(body["device_id"], body["transport"])
                    result = controller.snapshot()
                elif action == "disconnect":
                    controller.disconnect()
                    result = controller.snapshot()
                elif action in {"set", "clear"}:
                    coordinate = Coordinate(**body["coordinate"]) if action == "set" else None
                    result = controller.execute(body["event_id"], coordinate)
                elif action == "status":
                    result = controller.snapshot()
                else:
                    return self.reply(400, {"error": "unknown_action"})
                return self.reply(200, result)
            except (ValueError, TypeError, KeyError):
                return self.reply(400, {"error": "invalid_request"})
            except GatewayError as error:
                return self.reply(409, {"error": error.code, "message": str(error)})
            except Exception:
                return self.reply(500, {"error": "internal_error"})

    return ThreadingHTTPServer(address, Handler)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()
    gateway = DemoGateway() if args.demo else PmdGateway()
    server = make_server(
        (args.host, args.port), Controller(gateway), os.environ.get("QUICKMAPGO_AGENT_TOKEN", "")
    )
    print(f"Agente {'DEMO' if args.demo else 'EXPERIMENTAL'} em {args.host}:{args.port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Agente encerrado. A localização do aparelho não foi restaurada automaticamente.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
