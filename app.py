import os
from datetime import datetime
from pathlib import Path
from uuid import uuid4

import streamlit as st
import streamlit.components.v1 as components

import quickmapgo
from quickmapgo.core import Controller, Coordinate, DemoGateway, GatewayError
from quickmapgo.device import PmdGateway
from quickmapgo.remote import AgentClient

st.set_page_config(page_title="QuickMapGo", page_icon="📍", layout="wide")


@st.cache_resource
def get_service(mode, agent_url, token):
    if mode == "agent":
        if not agent_url or len(token) < 32:
            raise ValueError("Configure URL e token de pelo menos 32 caracteres para o agente.")
        return AgentClient(agent_url, token)
    if mode not in {"demo", "native"}:
        raise ValueError("QUICKMAPGO_MODE deve ser demo, native ou agent.")
    return Controller(DemoGateway() if mode == "demo" else PmdGateway())


map_component = components.declare_component(
    "quickmapgo_map", path=str(Path(quickmapgo.__file__).parent / "ui" / "map")
)
mode = os.getenv("QUICKMAPGO_MODE", "demo")
try:
    service = get_service(
        mode, os.getenv("QUICKMAPGO_AGENT_URL", ""), os.getenv("QUICKMAPGO_AGENT_TOKEN", "")
    )
except ValueError as error:
    st.error(str(error))
    st.stop()

st.title("📍 QuickMapGo")
st.caption("Selecione um ponto no mapa e acompanhe a última instrução.")
if mode == "demo":
    st.info("DEMONSTRAÇÃO — nenhuma instrução é enviada a um iPhone.")
else:
    st.warning("Integração experimental. Envio ao serviço não confirma aceitação pelo Pokémon GO.")

if "devices" not in st.session_state:
    st.session_state.devices = []
if "consumed_event" not in st.session_state:
    st.session_state.consumed_event = None

with st.sidebar:
    st.subheader("Conexão")
    transport = st.selectbox(
        "Transporte",
        ["usb", "wifi"],
        format_func=lambda value: "Cabo USB" if value == "usb" else "Wi-Fi",
    )
    if st.session_state.get("discovered_transport") != transport:
        st.session_state.devices = []
        st.session_state.discovered_transport = transport
    if st.button("Atualizar dispositivos", use_container_width=True):
        try:
            with st.spinner("Procurando dispositivos…"):
                st.session_state.devices = service.discover(transport)
        except GatewayError as error:
            st.session_state.devices = []
            st.error(str(error))
    devices = st.session_state.devices
    selected = st.selectbox(
        "Dispositivo",
        devices,
        index=0 if devices else None,
        format_func=lambda d: f"{d['name']} · …{d['id'][-4:]}",
        placeholder="Atualize a lista",
    )
    if st.button("Conectar", disabled=selected is None, use_container_width=True):
        try:
            with st.spinner("Verificando conexão…"):
                service.connect(selected["id"], transport)
        except GatewayError as error:
            st.error(str(error))
    if st.button("Desconectar", use_container_width=True):
        try:
            service.disconnect()
        except GatewayError as error:
            st.error(str(error))
    st.caption("Wi-Fi pode exigir configuração inicial por USB. No modo Wi-Fi, retire o cabo.")

try:
    state = service.snapshot()
except GatewayError as error:
    st.error(str(error))
    st.stop()

connected = bool(state["connection"])
if state.get("demo") and mode != "demo":
    st.info("O agente está em DEMONSTRAÇÃO; nenhum envio real ocorre.")
if connected:
    connection = state["connection"]
    st.success(f"Conectado · {connection['transport'].upper()} · …{connection['device_id'][-4:]}")
else:
    st.info("Nenhum dispositivo conectado.")

if st.button("Encerrar simulação", disabled=not connected):
    try:
        with st.spinner("Solicitando encerramento…"):
            result = service.execute(str(uuid4()), None)
        (st.success if result["status"] == "sent" else st.error)(result["message"])
        state = service.snapshot()
    except GatewayError as error:
        st.error(str(error))

event = map_component(
    last_attempt=state["last_attempt"],
    connected=connected,
    consumed_event=st.session_state.consumed_event,
    key="map",
    default=None,
)
if event and event["event_id"] != st.session_state.consumed_event:
    # Consumir mesmo em falha/busy: outro rerun jamais transforma o evento em retry.
    st.session_state.consumed_event = event["event_id"]
    try:
        with st.spinner("Enviando instrução…"):
            result = service.execute(
                event["event_id"], Coordinate(event["latitude"], event["longitude"])
            )
        st.session_state.pop("last_ui_error", None)
    except (GatewayError, ValueError) as error:
        st.session_state.last_ui_error = str(error)
    st.rerun()

if st.session_state.get("last_ui_error"):
    st.error(st.session_state.last_ui_error)
attempt = state["last_attempt"]
st.subheader("Última instrução")
if attempt:
    coordinate = attempt["coordinate"]
    columns = st.columns(3)
    columns[0].metric("Latitude", f"{coordinate['latitude']:.6f}")
    columns[1].metric("Longitude", f"{coordinate['longitude']:.6f}")
    labels = {"sent": "Enviado", "failed": "Falhou", "uncertain": "Incerto", "pending": "Enviando"}
    columns[2].metric("Estado", labels[attempt["status"]])
    timestamp = datetime.fromisoformat(attempt["requested_at"]).astimezone()
    st.caption(f"{timestamp:%d/%m/%Y %H:%M:%S %Z} · ID {attempt['id']}")
    st.write(attempt["message"])
    success = state["last_success"]
    if success and success["id"] != attempt["id"]:
        st.caption(f"Último sucesso anterior: {success['coordinate']} · {success['requested_at']}")
else:
    st.write("Clique no mapa após conectar um dispositivo.")
st.caption(
    f"Estado da simulação: {state['simulation_state']}. Desconectar não encerra a simulação."
)
