import math
from threading import Event, Thread

import pytest

from quickmapgo.core import Controller, Coordinate, DemoGateway, GatewayError


class RecordingGateway(DemoGateway):
    def __init__(self):
        self.calls = []
        self.error = None

    def apply(self, device_id, transport, coordinate):
        self.calls.append(coordinate)
        if self.error:
            raise self.error


@pytest.fixture
def controller():
    service = Controller(RecordingGateway())
    service.connect("demo-iphone", "usb")
    return service


@pytest.mark.parametrize("lat,lon", [(91, 0), (0, 181), (math.nan, 0), (0, math.inf), (True, 0)])
def test_invalid_coordinates(lat, lon):
    with pytest.raises(ValueError):
        Coordinate(lat, lon)


def test_coordinate_limits():
    Coordinate(-90, -180)
    Coordinate(90, 180)


def test_rerun_is_idempotent_but_new_click_same_position_sends(controller):
    point = Coordinate(-7, -34)
    first = controller.execute("click-1", point)
    assert controller.execute("click-1", point) is first
    controller.execute("click-2", point)
    assert controller.gateway.calls == [point, point]


def test_reusing_id_with_other_point_is_rejected(controller):
    controller.execute("one", Coordinate(1, 1))
    with pytest.raises(ValueError):
        controller.execute("one", Coordinate(2, 2))
    assert len(controller.gateway.calls) == 1


def test_failure_keeps_previous_success_and_timeout_never_retries(controller):
    first = controller.execute("one", Coordinate(1, 1))
    controller.gateway.error = GatewayError("timeout", "Incerto", uncertain=True)
    failed = controller.execute("two", Coordinate(2, 2))
    assert failed["status"] == "uncertain"
    assert controller.last_success is first
    assert controller.last_attempt is failed
    controller.execute("two", Coordinate(2, 2))
    assert len(controller.gateway.calls) == 2


def test_clear_and_disconnect_are_distinct(controller):
    controller.execute("set", Coordinate(1, 1))
    controller.execute("clear", None)
    assert controller.simulation_state == "clear_acknowledged"
    assert controller.last_attempt["id"] == "set"
    controller.disconnect()
    assert controller.simulation_state == "unknown"
    with pytest.raises(GatewayError):
        controller.execute("next", Coordinate(2, 2))


def test_two_sessions_cannot_send_or_disconnect_concurrently(controller):
    entered, release = Event(), Event()

    def slow_apply(**_):
        entered.set()
        assert release.wait(2)

    controller.gateway.apply = slow_apply
    thread = Thread(target=lambda: controller.execute("one", Coordinate(1, 1)))
    thread.start()
    assert entered.wait(2)
    try:
        with pytest.raises(GatewayError, match="andamento"):
            controller.execute("two", None)
        with pytest.raises(GatewayError):
            controller.disconnect()
    finally:
        release.set()
        thread.join()
