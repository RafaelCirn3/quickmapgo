from pathlib import Path

from streamlit.testing.v1 import AppTest


def test_demo_app_loads_and_connects_without_hardware(monkeypatch):
    monkeypatch.setenv("QUICKMAPGO_MODE", "demo")
    app = AppTest.from_file(Path(__file__).resolve().parents[1] / "app.py").run()
    assert not app.exception
    next(button for button in app.button if button.label == "Atualizar dispositivos").click().run()
    assert not app.exception
    next(button for button in app.button if button.label == "Conectar").click().run()
    assert not app.exception
    assert any("Conectado" in item.value for item in app.success)
