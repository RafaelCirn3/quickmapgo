import json
from threading import Thread
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import pytest

from quickmapgo.agent import make_server
from quickmapgo.core import Controller, Coordinate, DemoGateway
from quickmapgo.remote import AgentClient


@pytest.fixture
def agent():
    controller = Controller(DemoGateway())
    token = "test-only-" + "x" * 32
    server = make_server(("127.0.0.1", 0), controller, token)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    url = f"http://127.0.0.1:{server.server_address[1]}"
    yield AgentClient(url, token), url, controller
    server.shutdown()
    server.server_close()
    thread.join()


def test_agent_roundtrip_and_duplicate_event(agent):
    client, _, controller = agent
    devices = client.discover("wifi")
    client.connect(devices[0]["id"], "wifi")
    point = Coordinate(-7, -34)
    result = client.execute("map-click", point)
    assert result["status"] == "sent"
    assert client.execute("map-click", point) == result
    assert len(controller.operations) == 1
    assert client.snapshot()["demo"] is True
    assert client.execute("clear", None)["status"] == "sent"
    client.disconnect()
    assert client.snapshot()["connection"] is None


def test_agent_denies_missing_authentication(agent):
    _, url, _ = agent
    request = Request(url + "/api", data=b'{"action":"status"}', method="POST")
    with pytest.raises(HTTPError) as error:
        urlopen(request)
    assert error.value.code == 401


def test_agent_rejects_invalid_coordinates_without_side_effect(agent):
    client, url, controller = agent
    client.connect("demo-iphone", "usb")
    request = Request(
        url + "/api",
        method="POST",
        headers={"Authorization": f"Bearer {client.token}", "Content-Type": "application/json"},
        data=json.dumps(
            {"action": "set", "event_id": "bad", "coordinate": {"latitude": 91, "longitude": 0}}
        ).encode(),
    )
    with pytest.raises(HTTPError) as error:
        urlopen(request)
    assert error.value.code == 400
    assert not controller.operations
