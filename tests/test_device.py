import json
import subprocess
import sys
from types import SimpleNamespace

import pytest

from quickmapgo.core import Coordinate, GatewayError
from quickmapgo.device import PmdGateway


def test_discovery_is_filtered_and_does_not_use_shell():
    calls = []

    def run(args, **kwargs):
        calls.append((args, kwargs))
        return SimpleNamespace(
            returncode=0,
            stdout=json.dumps(
                [{"Identifier": "id", "DeviceName": "Phone", "ProductVersion": "26.6.2"}]
            ),
        )

    gateway = PmdGateway(runner=run)
    assert gateway.discover("wifi")[0]["id"] == "id"
    assert calls[0][0][-1] == "--network"
    assert "shell" not in calls[0][1]


def test_wifi_refuses_cable_instead_of_silently_using_usb():
    gateway = PmdGateway()
    gateway.discover = lambda transport: [{"id": "id"}]
    with pytest.raises(GatewayError, match="Retire o cabo"):
        gateway.check("id", "wifi")


def test_timeout_after_mutation_is_uncertain():
    def run(*args, **kwargs):
        raise subprocess.TimeoutExpired("pmd", 30)

    with pytest.raises(GatewayError) as error:
        PmdGateway(runner=run)._run(["clear"], mutating=True)
    assert error.value.uncertain


def test_set_selects_exact_device_and_handles_negative_coordinates():
    gateway = PmdGateway()
    gateway.check = lambda *_: None
    captured = []
    gateway._set = captured.append
    gateway.apply("chosen-id", "usb", Coordinate(-7, -34))
    assert captured[0][-5:] == ["--udid", "chosen-id", "--", "-7", "-34"]


def test_worker_acknowledgement_keeps_context_alive_until_close(monkeypatch):
    original = subprocess.Popen

    def spawn(args, **kwargs):
        return original(
            [sys.executable, "-u", "-c", "print('__QUICKMAPGO_APPLIED__', flush=True); input()"],
            **kwargs,
        )

    monkeypatch.setattr("quickmapgo.device.subprocess.Popen", spawn)
    gateway = PmdGateway(timeout=2)
    gateway._set([])
    process = gateway.process
    assert process.poll() is None
    gateway.close()
    assert process.poll() == 0
