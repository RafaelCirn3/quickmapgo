from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from math import isfinite
from threading import Lock
from typing import Protocol


class GatewayError(Exception):
    def __init__(self, code: str, message: str, uncertain: bool = False):
        super().__init__(message)
        self.code = code
        self.uncertain = uncertain


@dataclass(frozen=True)
class Coordinate:
    latitude: float
    longitude: float

    def __post_init__(self):
        if (
            isinstance(self.latitude, bool)
            or isinstance(self.longitude, bool)
            or not isfinite(self.latitude)
            or not isfinite(self.longitude)
            or not -90 <= self.latitude <= 90
            or not -180 <= self.longitude <= 180
        ):
            raise ValueError("Coordenadas inválidas.")


class Gateway(Protocol):
    def discover(self, transport: str) -> list[dict]: ...
    def check(self, device_id: str, transport: str) -> None: ...
    def apply(self, device_id: str, transport: str, coordinate: Coordinate | None) -> None: ...


def validate_transport(transport: str):
    if transport not in {"usb", "wifi"}:
        raise ValueError("Transporte inválido.")


class DemoGateway:
    def discover(self, transport):
        validate_transport(transport)
        return [{"id": "demo-iphone", "name": "iPhone de demonstração", "ios_version": "simulado"}]

    def check(self, device_id, transport):
        validate_transport(transport)
        if device_id != "demo-iphone":
            raise GatewayError("device_not_found", "Dispositivo de demonstração não encontrado.")

    def apply(self, device_id, transport, coordinate):
        self.check(device_id, transport)


class Controller:
    """Um controlador por processo: bloqueio e deduplicação inclusive entre abas."""

    def __init__(self, gateway: Gateway):
        self.gateway = gateway
        self.lock = Lock()
        self.connection = None
        self.operations = {}
        self.last_attempt = None
        self.last_success = None
        self.simulation_state = "unknown"

    def discover(self, transport):
        validate_transport(transport)
        return self.gateway.discover(transport)

    def connect(self, device_id, transport):
        validate_transport(transport)
        if not self.lock.acquire(blocking=False):
            raise GatewayError("operation_busy", "Há uma operação em andamento.")
        try:
            self.gateway.check(device_id, transport)
            self.connection = {"device_id": device_id, "transport": transport}
        finally:
            self.lock.release()

    def disconnect(self):
        if not self.lock.acquire(blocking=False):
            raise GatewayError("operation_busy", "Há uma operação em andamento.")
        try:
            close = getattr(self.gateway, "close", None)
            if close:
                close()
            self.connection = None
            self.simulation_state = "unknown"
        finally:
            self.lock.release()

    def execute(self, event_id: str, coordinate: Coordinate | None):
        if not isinstance(event_id, str) or not 1 <= len(event_id) <= 128:
            raise ValueError("Evento inválido.")
        if not self.lock.acquire(blocking=False):
            raise GatewayError("operation_busy", "Há uma operação em andamento; clique ignorado.")
        try:
            signature = asdict(coordinate) if coordinate else None
            if event_id in self.operations:
                previous = self.operations[event_id]
                if previous[0] != signature:
                    raise ValueError("ID de evento reutilizado com dados diferentes.")
                return previous[1]
            if not self.connection:
                raise GatewayError("device_disconnected", "Conecte um dispositivo antes de enviar.")
            operation = {
                "id": event_id,
                "coordinate": signature,
                "requested_at": datetime.now(UTC).isoformat(),
                "status": "pending",
                "action": "set" if coordinate else "clear",
                "message": "Enviando…",
            }
            # Reservar antes do efeito externo evita retry em uma resposta perdida.
            self.operations[event_id] = (signature, operation)
            if coordinate:
                self.last_attempt = operation
            try:
                self.gateway.apply(**self.connection, coordinate=coordinate)
                operation.update(
                    status="sent",
                    message=(
                        "Instrução enviada ao serviço."
                        if coordinate
                        else "Encerramento confirmado pelo serviço. Verifique o aplicativo."
                    ),
                )
                self.simulation_state = "possibly_active" if coordinate else "clear_acknowledged"
                if coordinate:
                    self.last_success = operation
            except GatewayError as error:
                operation.update(
                    status="uncertain" if error.uncertain else "failed",
                    message=str(error),
                    error_code=error.code,
                )
                if error.uncertain:
                    self.simulation_state = "unknown"
                if error.code in {"device_disconnected", "device_not_found"}:
                    self.connection = None
            except Exception:
                # Efeito externo pode ter ocorrido antes de uma exceção inesperada.
                operation.update(
                    status="uncertain",
                    message="Resultado não confirmado.",
                    error_code="internal_error",
                )
                self.simulation_state = "unknown"
            operation["completed_at"] = datetime.now(UTC).isoformat()
            return operation
        finally:
            self.lock.release()

    def snapshot(self):
        return {
            "connection": self.connection,
            "last_attempt": self.last_attempt,
            "last_success": self.last_success,
            "simulation_state": self.simulation_state,
            "demo": isinstance(self.gateway, DemoGateway),
        }
