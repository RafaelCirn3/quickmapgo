# Requisitos e critérios de aceite

Todos os requisitos estão planejados, sem implementação. P0 = essencial ao MVP; P1 = apoio ao desenvolvimento.

## Funcionais

| ID | Prioridade | Requisito | Critério de aceite |
| --- | --- | --- | --- |
| RF01 | P0 | Executar painel local Streamlit | Abrir em 127.0.0.1 na porta configurada; erro de porta ocupada é compreensível |
| RF02 | P0 | Renderizar mapa 2D | Zoom e arraste funcionam; atribuição do provedor permanece visível |
| RF03 | P0 | Selecionar dispositivo | Listar aparelhos descobertos; nunca enviar ao primeiro aparelho implicitamente |
| RF04 | P0 | Conectar por USB | Selecionar USB, conectar ao aparelho autorizado e mostrar estado pronto ou causa da falha |
| RF05 | P0 | Conectar por Wi-Fi | Mesmo fluxo via rede, com pareamento/pré-requisitos documentados; funcionar sem cabo após preparação |
| RF06 | P0 | Enviar pelo clique | Cada evento novo válido, com conexão pronta, gera no máximo uma tentativa |
| RF07 | P0 | Indicar última instrução | Marcador exibe coordenadas, horário e estado pendente/enviado/falhou/incerto |
| RF08 | P0 | Separar tentativa e sucesso | Falha atualiza marcador da tentativa, mas preserva o último sucesso como informação separada |
| RF09 | P0 | Encerrar simulação | Solicitar clear; exibir sucesso, falha ou resultado incerto sem alegar restauração se não confirmada |
| RF10 | P0 | Tratar desconexão | Bloquear novos envios, informar perda de conexão e permitir reconectar |
| RF11 | P0 | Validar coordenadas | Rejeitar valores não finitos, latitude fora de [-90,90] e longitude fora de [-180,180] |
| RF12 | P1 | Modo demonstração | Clicar sem aparelho usando adaptador falso; mostrar permanentemente que não há envio real |

## Não funcionais

| ID | Requisito verificável |
| --- | --- |
| RNF01 | Rodar nativamente no Windows; validar versões exatas na matriz de compatibilidade |
| RNF02 | Vincular servidor a 127.0.0.1; não exigir exposição pública para conexão Wi-Fi do aparelho |
| RNF03 | Não versionar registros de pareamento, identificadores completos, logs privados ou coordenadas reais |
| RNF04 | Uma operação mutável por dispositivo de cada vez, inclusive entre abas do navegador |
| RNF05 | Timeout inicial proposto de 15 s, configurável e revisado após a prova; sem repetição automática de set/clear |
| RNF06 | Reexecução do Streamlit, zoom, arraste ou atualização visual não podem repetir comandos |
| RNF07 | Mapas dependem de internet conforme provedor; falha de tiles deve manter controles/status utilizáveis |
| RNF08 | Código de interface não depende diretamente das APIs de iOS; o adaptador é substituível em testes |
| RNF09 | Dependências fixadas somente após validação, com versões e procedimento reproduzível registrados |

## Regras de negócio

- Enviar exige dispositivo escolhido, conexão pronta e coordenada válida.
- Cada operação recebe ID único; rerun reutiliza o evento processado, sem criar outra operação.
- Um novo clique na mesma coordenada deve ser permitido se for um novo evento. A detecção não pode depender apenas do par latitude/longitude.
- Durante envio ou encerramento, ignorar novos cliques com aviso de operação em andamento; não acumular fila oculta.
- Retorno positivo do adaptador significa instrução enviada, não confirmação do GPS real nem aceitação pelo jogo.
- Timeout após despacho produz estado incerto: a instrução pode ter sido aplicada. Não repetir automaticamente.
- Após desconectar/reiniciar, o estado do aparelho é desconhecido; não assumir que a localização real foi restaurada.
