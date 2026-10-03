# Viabilidade, riscos e compatibilidade

## Estado em 02/10/2026

A documentação upstream descreve simulação de localização e transportes USB/Wi-Fi. Isso não confirma funcionamento neste iPhone com iOS 26.6.2 nem no Pokémon GO. Nenhum teste físico foi executado nesta preparação.

## Matriz de evidências

| Ambiente | Transporte | Descoberta/conexão | Set | Clear | Consumidor |
| --- | --- | --- | --- | --- | --- |
| Windows a identificar + iOS 26.6.2/build a confirmar | USB | Não testado | Não testado | Não testado | Pokémon GO não testado |
| Mesmo ambiente | Wi-Fi sem cabo após preparação | Não testado | Não testado | Não testado | Pokémon GO não testado |

Preencher com versão de Python, pacote, drivers, modelo do aparelho, data, procedimento e evidência sanitizada.

## Prova de viabilidade — primeiro trabalho de desenvolvimento

1. Registrar Windows, iPhone, versão/build do iOS e versões dos componentes.
2. Consultar instalação e transporte da versão atual da biblioteca; preparar drivers, autorização e serviços necessários.
3. Validar descoberta e conexão USB sem aplicar coordenadas.
4. Enviar uma coordenada de teste e observar separadamente retorno do serviço e localização apresentada por um consumidor.
5. Solicitar clear e registrar retorno e comportamento observado.
6. Preparar Wi-Fi conforme documentação; retirar cabo e repetir conexão, set e clear.
7. Verificar perda de rede, reconexão e timeout sem repetição automática.
8. Registrar resultado no modelo de experimento e atualizar matriz.

Se a simulação for aceita pelo serviço mas não pelo jogo, registrar “envio validado; objetivo no consumidor não validado”. Não classificar o projeto como funcional para Pokémon GO.

## Critério para avançar

Adaptador real do MVP exige evidência de conectar, set e clear nos dois transportes. A interface em demonstração pode avançar independentemente. Falha em um transporte exige investigação ou revisão explícita de escopo; não marcar MVP completo com um transporte ausente.

## Riscos e resposta

| Risco | Impacto | Resposta |
| --- | --- | --- |
| Incompatibilidade iOS/biblioteca | Bloqueia dispositivo | Prova física antes do adaptador; fixar versões validadas |
| Aplicativo rejeita simulação | Objetivo de uso não alcançado | Teste separado; não inferir aceitação nem incluir ocultação da simulação |
| Rerun repete comando | Envios inesperados | IDs de eventos, estado e testes de rerun |
| Cliques rápidos e abas concorrentes | Ordem incorreta | Bloqueio por dispositivo; sem fila silenciosa |
| Timeout com efeito já aplicado | Estado desconhecido | Resultado incerto, sem retry; verificação manual |
| Desconexão deixa simulação ativa | Resultado inesperado | Clear explícito e procedimento de recuperação validado |
| Tiles indisponíveis | Mapa não carrega | Mensagem e controles preservados; verificar regras do provedor |
| Atualização altera APIs | Quebra execução | Versões fixas e revalidação por ambiente |

## Modelo de registro de experimento

Copiar [modelo de experimento](templates/experimento.md). Nesta fase, comandos exatos do adaptador e privilégios necessários serão definidos a partir da versão testada, em vez de documentar uma receita universal não comprovada.
