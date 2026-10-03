# ADR 0001 — Aplicação local com Streamlit

Data: 02/10/2026. Estado: decisão inicial, parcialmente substituída pela [ADR 0002](0002-docker-agente-e-eventos.md) para mapa, Docker e integração. A opção Streamlit permanece; a integração física continua pendente.

## Contexto

O usuário definiu Windows, interface de mapa no navegador com porta explícita, Streamlit e conexões USB/Wi-Fi para um iPhone. A versão informada é iOS 26.6.2. O sistema deve mostrar a última instrução e não confundir envio com aceitação pelo jogo.

## Decisão

Usar aplicação local Python com Streamlit. Adotar Folium + streamlit-folium como candidata para mapa interativo e pymobiledevice3 como candidata para integração iOS. Separar domínio, serviço e gateway com implementações real e falsa.

Não adicionar FastAPI ou SPA ao MVP. Executar painel em 127.0.0.1:8501, com porta configurável. Wi-Fi é transporte do dispositivo, não publicação do painel.

## Consequências

- Menor infraestrutura e interface escrita em Python.
- Reexecuções do Streamlit exigem consumo explícito de eventos e proteção de efeitos externos.
- Hardware e serviços locais continuam necessários; hospedar apenas o painel na nuvem não resolve a comunicação.
- Persistência inicialmente em memória; reinício deixa o estado do aparelho desconhecido.
- Na decisão inicial, versões e integração API/CLI seriam escolhidas após testes. A implementação experimental fixou versões diretas e CLI/worker na ADR 0002; a validação física permanece pendente.
- Se o componente não representar novos cliques na mesma coordenada, adaptar a captura de eventos mantendo o comportamento definido.

## Alternativas

HTML/Leaflet + FastAPI era uma alternativa discutida, substituída pela preferência explícita por Streamlit. React/Angular acrescentariam uma camada não solicitada. Bluetooth não faz parte do escopo validável inicial.
