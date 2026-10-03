# Validação da implementação inicial

Data: 02/10/2026 (America/Fortaleza).

## Fluxo avaliado

Clique no mapa Streamlit → evento com UUID → Controller local ou agente HTTP Windows → gateway → resultado e marcador. A prova automatizada usa gateway de demonstração; não há aparelho conectado neste ambiente.

## Evidências locais

| Camada | Resultado | Evidência |
| --- | --- | --- |
| Python | Aprovado | 20 testes pytest passaram |
| Estilo/importações | Aprovado | ruff check e format sem pendências |
| Streamlit | Aprovado no teste de aplicação | AppTest carrega UI, descobre e conecta dispositivo de demonstração |
| Eventos do mapa | Aprovado em teste JavaScript | 1 teste Node: gesto único, bloqueio até confirmação e repetição de coordenada com ID diferente |
| Ponte HTTP | Aprovado em loopback | Teste com servidor real: autenticação, descoberta, conexão, set, deduplicação, clear e desconexão |
| Worker de dispositivo | Aprovado com processo substituto | Mantém processo vivo após confirmação e fecha quando solicitado |
| Servidor Streamlit | Aprovado | Inicialização e endpoint /_stcore/health retornou ok |
| Sintaxe do Compose | Aprovada por parser YAML | Serviço web, publicação local e read-only verificados |
| Docker build/container | Não executado localmente | Docker indisponível no ambiente; CI contém build, start e healthcheck |
| Navegador visual | Pendente | agent-browser não iniciou; download do Chromium do Playwright retornou arquivo inválido |
| iPhone USB/Wi-Fi | Não testado | Sem acesso físico ao aparelho/Windows do usuário |
| Pokémon GO | Não testado | Aceitação pelo consumidor não inferida de demonstração ou envio |

O teste Node verifica lógica de eventos com DOM/Leaflet substitutos; não comprova renderização de tiles ou iframe num navegador real. O teste de subprocesso substituto não comprova serviços Apple ou comportamento DVT. A CLI da versão instalada foi inspecionada via --help, sem enviar ao aparelho.

## Pendências antes de considerar o MVP concluído

- Rodar CI e registrar resultado de Docker.
- Verificar visualmente mapa, clique e marcador no navegador do Windows.
- Preencher a matriz física de descoberta, set, clear e reconexão em USB e Wi-Fi.
- Confirmar comunicação do Docker Desktop com o agente host; execução nativa disponível como alternativa.
- Medir responsividade durante descoberta/serviços iOS, que usam chamadas síncronas nesta versão.
- Validar o worker persistente e a recuperação após encerramento/desconexão.
- Avaliar separadamente a localização aceita pelo aplicativo consumidor.

## Limitações conhecidas

Versões diretas fixadas, sem lockfile transitivo. Estado/histórico em memória sem retenção permanente. Wi-Fi depende de descoberta usbmux do serviço Apple, sem fallback Bonjour. Ausência de polling de saúde do dispositivo: perda de conexão é detectada durante uma verificação/operação. Mudanças feitas por outra aba aparecem na próxima reexecução.
