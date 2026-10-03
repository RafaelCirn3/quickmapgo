# Casos de uso e interface

## UC01 — Preparar conexão (RF03–RF05)

Operador escolhe USB ou Wi-Fi, solicita descoberta, seleciona o iPhone e conecta. O serviço verifica prontidão. Se faltarem autorização, driver, modo desenvolvedor ou túnel, exibe orientação baseada no erro observado. Nenhum envio de coordenada ocorre ao conectar.

Wi-Fi pode exigir pareamento inicial por USB e configuração da comunicação de rede. A necessidade exata será confirmada na prova de viabilidade. Falha de Wi-Fi não muda automaticamente para USB.

## UC02 — Enviar ponto (RF02, RF06–RF08, RF11)

Pré-condição: conexão pronta, nenhuma operação em andamento.

1. Operador clica no mapa.
2. UI recebe evento novo e valida latitude/longitude.
3. Serviço registra tentativa e mostra marcador pendente.
4. Adaptador executa uma única operação.
5. UI atualiza o marcador e detalhes com sucesso, falha ou resultado incerto.

Zoom/arraste e reexecuções não contam como cliques novos. Clique com conexão indisponível informa que nenhum envio foi realizado. O mapa não deve mover o marcador por uma simples navegação.

## UC03 — Encerrar simulação (RF09)

Operador solicita encerramento. Controles de envio ficam bloqueados enquanto clear é executado. Em sucesso, mostrar “Simulação encerrada pelo serviço”. Em falha/timeout, manter estado não confirmado e orientação para verificação manual. O encerramento não garante atualização imediata do aplicativo consumidor.

## UC04 — Perder conexão (RF10)

Perda detectada atualiza estado e bloqueia envio. Coordenadas anteriores permanecem como histórico da sessão, identificadas como resultado passado. Reconexão exige seleção/validação do dispositivo; não reenviar a última posição automaticamente.

## Organização da tela

| Área | Conteúdo |
| --- | --- |
| Barra lateral | Transporte, atualizar dispositivos, aparelho escolhido, conectar/desconectar, modo demonstração |
| Área principal | Mapa 2D com zoom e um marcador da última tentativa |
| Detalhes | Latitude, longitude, horário, ID da operação, estado e mensagem |
| Informação secundária | Última instrução enviada com sucesso, se diferente da tentativa atual |
| Ação | Encerrar simulação |
| Rodapé | Estado da conexão e atribuição do mapa |

Estados do marcador: pendente (âmbar), enviado (verde), falhou (vermelho), incerto (cinza). Sempre apresentar rótulo textual além da cor.

Sem instruções: “Clique no mapa após conectar um dispositivo”. Em demonstração: “Demonstração: nenhuma instrução enviada ao iPhone”.

## Decisão adotada na implementação

O componente próprio com Leaflet gera UUID por gesto. Durante o envio ele bloqueia novos cliques até o evento ser consumido. Reexecuções recebem o mesmo ID e não repetem a operação. Ver ADR 0002.
