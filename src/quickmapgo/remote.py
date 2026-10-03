import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from quickmapgo.core import GatewayError


class AgentClient:
    def __init__(self, url, token):
        self.url = url.rstrip("/")
        self.token = token

    def call(self, action, **data):
        request = Request(
            self.url + "/api",
            data=json.dumps({"action": action, **data}).encode(),
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {self.token}"},
            method="POST",
        )
        try:
            with urlopen(request, timeout=100) as response:
                return json.load(response)
        except HTTPError as error:
            payload = json.load(error)
            raise GatewayError(
                payload.get("error", "agent_rejected"),
                payload.get("message", f"Agente recusou a solicitação (HTTP {error.code})."),
            ) from error
        except (URLError, TimeoutError) as error:
            raise GatewayError(
                "agent_unavailable",
                "Agente indisponível; resultado não confirmado.",
                uncertain=action in {"set", "clear"},
            ) from error

    def discover(self, transport):
        return self.call("discover", transport=transport)["devices"]

    def connect(self, device_id, transport):
        return self.call("connect", device_id=device_id, transport=transport)

    def disconnect(self):
        return self.call("disconnect")

    def execute(self, event_id, coordinate):
        return self.call(
            "set" if coordinate else "clear",
            event_id=event_id,
            coordinate={"latitude": coordinate.latitude, "longitude": coordinate.longitude}
            if coordinate
            else None,
        )

    def snapshot(self):
        return self.call("status")
