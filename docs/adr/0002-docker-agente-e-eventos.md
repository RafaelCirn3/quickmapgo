# ADR 0002 — Docker, agente Windows e eventos de mapa

Data: 02/10/2026. Estado: implementada na versão inicial; integração física ainda experimental.

## Contexto

O usuário solicitou Docker Compose ao iniciar a implementação. Um container Linux do Docker Desktop não herda automaticamente os drivers e serviços Apple do Windows. O envio ao aparelho deve continuar nativo.

O requisito de repetir um clique na mesma coordenada também exige identificar cada gesto, independentemente dos valores de latitude/longitude.

## Decisão

- Docker Compose executa o painel Streamlit, em demonstração por padrão.
- Modo nativo pode executar painel e adaptador no Windows.
- Modo agente permite painel em Docker e comunicação HTTP autenticada com um processo Python no Windows.
- Agente usa biblioteca padrão HTTP, sem FastAPI e sem comandos arbitrários vindos da interface.
- UI local no host em 127.0.0.1; agente também começa em loopback. Acessibilidade por host.docker.internal deve ser testada no Docker Desktop instalado.
- Se o agente não estiver acessível pelo container, usar execução inteiramente nativa ou um endereço específico de interface do host com firewall restrito. Não abrir o agente em todas as interfaces automaticamente.
- Mapa usa componente Streamlit próprio com Leaflet 1.9.4 e UUID por clique. Folium/streamlit-folium eram candidatas, substituídas para garantir a semântica de eventos sem deduplicação por coordenada.
- Adaptador experimental usa CLI pymobiledevice3 11.20.2 e worker persistente. A CLI chama wait_return após o envio; o worker emite confirmação nessa etapa e mantém o contexto aberto até troca/encerramento.

## Consequências e limites

Token de pelo menos 32 caracteres obrigatório no agente, sem armazenamento em Git. Não há exposição pública do painel no Compose. Sem montagem de USB ou modo privileged.

O worker depende de detalhe da versão fixada da biblioteca. Deve ser revalidado quando atualizá-la. Conexão pronta significa aparelho descoberto no transporte escolhido, não validação de todos os serviços DVT. Atualizações do aparelho podem invalidar o resultado.

O modo Wi-Fi recusa operação se o mesmo aparelho estiver conectado por USB, para evitar seleção silenciosa do cabo. Descoberta Wi-Fi inicial depende do Apple Mobile Device Service; fallback Bonjour ainda não foi implementado.

O agente centraliza bloqueio e IDs de operações entre clientes. Reiniciá-lo perde o histórico em memória e torna o estado do aparelho desconhecido. Desconectar não equivale a clear; fechar o worker pode alterar o comportamento da simulação e exige observação real.
