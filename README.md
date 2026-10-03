# QuickMapGo

Painel local em Python/Streamlit para escolher uma posição num mapa e solicitar simulação de localização em um iPhone conectado ao Windows por **USB ou Wi-Fi**.

**Versão inicial implementada. Demonstração disponível; integração física com iOS 26.6.2 e Pokémon GO ainda não validada.**

## Iniciar com Docker Compose

Com Docker Desktop em execução, na pasta do projeto:

```powershell
Copy-Item .env.example .env
docker compose up --build -d
```

Abrir http://127.0.0.1:8501. Atualizar dispositivos, conectar o aparelho de demonstração e clicar no mapa. O modo padrão não envia instruções a um iPhone real.

```powershell
docker compose ps
docker compose logs -f web
docker compose down
```

## Funcionalidades iniciais

- Streamlit em português, mapa Leaflet visto de cima, zoom e navegação.
- Clique com ID único: novos cliques no mesmo ponto são permitidos, reruns não repetem envio.
- Marcador da última tentativa, coordenadas, horário e resultado.
- Último sucesso separado da tentativa que falhou.
- Seleção USB/Wi-Fi, descoberta, conexão e encerramento.
- Adaptador de demonstração, adaptador iOS experimental e agente Windows autenticado.
- Bloqueio de operações simultâneas e timeout sem retry automático.
- Testes e CI para Python e build/healthcheck do Compose.

## Docker e iPhone

O container executa o **painel**. Drivers e serviços Apple permanecem no Windows. Para um aparelho real, usar execução nativa ou painel Docker + agente nativo Windows. Não há passagem USB automática para container Linux nem serviço privilegiado.

O envio ao serviço não comprova aceitação pelo Pokémon GO. A conexão exibida confirma descoberta no transporte; a aplicação de coordenadas depende dos serviços de desenvolvimento do aparelho.

## Executar nativamente no Windows

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
$env:QUICKMAPGO_MODE = "demo"
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Consultar o [guia Windows/Docker](docs/09-execucao-windows-docker.md) para o extra device, agente, token e configuração USB/Wi-Fi. O mapa depende de internet para carregar Leaflet e tiles OpenStreetMap.

## Stack

| Componente | Implementação |
| --- | --- |
| UI | Streamlit 1.65.0 |
| Mapa | Componente bidirecional próprio + Leaflet 1.9.4 |
| iOS | pymobiledevice3 11.20.2, adaptador experimental com worker persistente |
| Ponte Docker/Windows | Agente HTTP da biblioteca padrão, autenticado por token |
| Estado | Memória do processo; sem banco |
| Execução | Python 3.12+, Windows ou painel Linux em Docker |

Folium/streamlit-folium foram candidatas iniciais; a decisão final está na ADR 0002. Dependências diretas estão fixadas; as transitivas ainda não têm lockfile.

## Documentação

- [Visão e escopo](docs/01-visao-escopo.md)
- [Requisitos e aceite](docs/02-requisitos.md)
- [Casos de uso e interface](docs/03-casos-de-uso-interface.md)
- [Arquitetura](docs/04-arquitetura.md)
- [Modelos e contratos](docs/05-modelos-contratos.md)
- [Viabilidade e riscos](docs/06-viabilidade-riscos.md)
- [Plano de desenvolvimento](docs/07-plano-desenvolvimento.md)
- [Testes](docs/08-testes.md)
- [Execução Windows/Docker](docs/09-execucao-windows-docker.md)
- [ADR 0001](docs/adr/0001-aplicacao-local-streamlit.md)
- [ADR 0002](docs/adr/0002-docker-agente-e-eventos.md)
- [Referências](docs/referencias.md)
- [Contribuição](CONTRIBUTING.md)

## Validação e próximos passos

Validar USB e Wi-Fi no ambiente real, registrar versões/builds e comportamento no consumidor. O modo demonstração e os testes automatizados não substituem essa prova. Consultar [relatório da implementação](docs/10-validacao-inicial.md) para evidências e pendências.

## Histórico

- 02/10/2026 (America/Fortaleza): engenharia inicial e primeira implementação com Streamlit, Docker Compose, agente e testes.
