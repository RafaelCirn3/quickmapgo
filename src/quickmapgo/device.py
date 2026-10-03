"""Adaptador experimental de CLI. Não executa shell nem comandos fornecidos pela UI."""

import json
import subprocess
import sys
from threading import Event, Thread

from quickmapgo.core import Coordinate, GatewayError, validate_transport


class PmdGateway:
    def __init__(self, timeout=30, runner=subprocess.run):
        self.timeout = timeout
        self.runner = runner
        self.process = None

    def close(self):
        process, self.process = self.process, None
        if process is None or process.poll() is not None:
            return
        try:
            process.stdin.write("\n")
            process.stdin.flush()
            process.wait(timeout=3)
        except (OSError, subprocess.TimeoutExpired):
            process.terminate()
            try:
                process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()

    def _set(self, args):
        self.close()
        done = Event()
        acknowledged = Event()
        self.process = subprocess.Popen(
            [sys.executable, "-u", "-m", "quickmapgo.device_worker", *args],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        process = self.process

        def consume():
            for line in process.stdout:
                if line.strip() == "__QUICKMAPGO_APPLIED__":
                    acknowledged.set()
                    done.set()
            done.set()

        Thread(target=consume, daemon=True).start()
        completed = done.wait(self.timeout)
        if not completed or not acknowledged.is_set():
            self.close()
            raise GatewayError(
                "timeout" if not completed else "device_command_failed",
                "Aplicação da localização não confirmada; verifique o aparelho.",
                uncertain=True,
            )

    def _run(self, args, mutating=False):
        try:
            result = self.runner(
                [sys.executable, "-m", "pymobiledevice3", *args],
                capture_output=True,
                text=True,
                timeout=self.timeout,
                stdin=subprocess.DEVNULL,
            )
        except subprocess.TimeoutExpired as error:
            raise GatewayError(
                "timeout", "Tempo esgotado; não repetir automaticamente.", uncertain=mutating
            ) from error
        except OSError as error:
            raise GatewayError(
                "driver_missing", "Não foi possível iniciar a biblioteca iOS."
            ) from error
        if result.returncode:
            # Não devolver saída bruta: pode conter UDID, coordenadas ou pareamento.
            raise GatewayError(
                "device_command_failed",
                "Serviço iOS recusou a operação. Verifique drivers, autorização e túnel.",
                uncertain=mutating,
            )
        return result.stdout

    def discover(self, transport):
        validate_transport(transport)
        output = self._run(["usbmux", "list", "--usb" if transport == "usb" else "--network"])
        try:
            devices = json.loads(output)
            return [
                {
                    "id": d["Identifier"],
                    "name": d.get("DeviceName", "iPhone"),
                    "ios_version": d.get("ProductVersion", "desconhecido"),
                }
                for d in devices
            ]
        except (ValueError, KeyError, TypeError) as error:
            raise GatewayError(
                "unsupported_environment", "Formato de descoberta incompatível."
            ) from error

    def check(self, device_id, transport):
        devices = self.discover(transport)
        if not any(d["id"] == device_id for d in devices):
            raise GatewayError(
                "device_not_found", "Aparelho indisponível no transporte selecionado."
            )
        if transport == "wifi" and any(d["id"] == device_id for d in self.discover("usb")):
            raise GatewayError("transport_unavailable", "Retire o cabo para usar o modo Wi-Fi.")

    def apply(self, device_id, transport, coordinate: Coordinate | None):
        self.check(device_id, transport)
        # Este primeiro adaptador destina-se ao serviço DVT de iOS 17+, incluindo a versão-alvo 26.
        args = [
            "developer",
            "dvt",
            "simulate-location",
            "set" if coordinate else "clear",
            "--udid",
            device_id,
        ]
        if coordinate:
            args.extend(["--", str(coordinate.latitude), str(coordinate.longitude)])
            self._set(args)
        else:
            self.close()
            self._run(args, mutating=True)
