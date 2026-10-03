# Executar no Windows e com Docker

## Demonstração com Docker Desktop

Na pasta do repositório, com Docker Desktop em execução:

```powershell
Copy-Item .env.example .env
docker compose up --build -d
docker compose ps
```

Abrir http://127.0.0.1:8501. Escolher transporte, atualizar dispositivos, conectar o iPhone de demonstração e clicar no mapa. O marcador acompanha a última tentativa. Nenhuma instrução é enviada a um aparelho nesse modo.

```powershell
docker compose logs -f web
docker compose down
```

Porta configurável por QUICKMAPGO_PORT em .env. O serviço publica apenas em 127.0.0.1. Internet é necessária para Leaflet e tiles OpenStreetMap. Dockerfile usa usuário sem privilégios e Compose inclui healthcheck, filesystem read-only e diretório temporário.

## Execução nativa

Python 3.12+ instalado:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
$env:QUICKMAPGO_MODE = "demo"
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Não é necessário ativar o ambiente virtual. Para testar o adaptador experimental:

```powershell
.\.venv\Scripts\python.exe -m pip install -e ".[device]"
$env:QUICKMAPGO_MODE = "native"
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Instalar/preparar o Apple Mobile Device Service e autorização conforme documentação da versão fixada de pymobiledevice3. Verificar necessidade de Modo Desenvolvedor, imagem de desenvolvimento e túnel. Esses pré-requisitos não são configurados automaticamente pelo QuickMapGo.

O comando abaixo habilita comunicação Wi-Fi conforme documentação upstream e deve ser executado com o aparelho autorizado e conectado por USB:

```powershell
.\.venv\Scripts\python.exe -m pymobiledevice3 lockdown wifi-connections on --udid SEU_UDID
```

Consultar --help da versão instalada antes do procedimento. Não publicar o UDID. Usar mesma rede, retirar o cabo e atualizar dispositivos no modo Wi-Fi. Se não aparecer, consultar limitações do serviço Apple/Bonjour na [referência de transporte](https://github.com/doronz88/pymobiledevice3/blob/master/docs/guides/ios17-tunnels.md). O fallback Bonjour não foi implementado nesta versão.

## Painel Docker + agente nativo Windows

Instalar o extra device no ambiente Windows, como acima. Gerar token no PowerShell:

```powershell
$env:QUICKMAPGO_AGENT_TOKEN = (& .\.venv\Scripts\python.exe -c "import secrets; print(secrets.token_urlsafe(32))")
.\.venv\Scripts\python.exe -m quickmapgo.agent
```

O agente inicia em 127.0.0.1:8765. Em outro terminal, colocar o mesmo token na variável QUICKMAPGO_AGENT_TOKEN de .env (arquivo ignorado pelo Git), configurar QUICKMAPGO_MODE=agent e manter QUICKMAPGO_AGENT_URL=http://host.docker.internal:8765. Recriar o painel:

```powershell
docker compose up --build -d --force-recreate
```

Testar “Atualizar dispositivos”. Se o Docker Desktop não alcançar o agente em loopback, preferir inicialmente a execução nativa. Para configurar acesso por uma interface específica do Windows, iniciar o agente com --host ENDERECO_DO_HOST e ajustar QUICKMAPGO_AGENT_URL, limitando o acesso no firewall à origem necessária. Não usar endereço público nem abrir a porta no roteador. Essa comunicação host/container ainda não foi validada no computador do usuário.

O painel não lê .env na execução nativa; nesse caso usar variáveis do PowerShell. O Compose lê .env. O agente deve receber o token pelo ambiente do terminal em que foi iniciado.

Para testar a ponte sem iPhone, iniciar o agente com --demo. O painel identifica esse estado como demonstração.

## Recuperação

“Encerrar simulação” solicita clear. Após sucesso, conferir o consumidor. Falhas e timeout não são repetidos automaticamente. Desconexão, fechamento do navegador ou reinício não confirmam restauração. Reconectar e solicitar clear; se o serviço falhar, registrar o ambiente e consultar recuperação upstream. Não há procedimento de recuperação física validado nesta entrega.

## Verificações

```powershell
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\ruff.exe check .
docker compose config --quiet
```

CI executa testes Python e build/healthcheck do Compose em Linux. Isso não valida USB/Wi-Fi com iPhone no Windows.
