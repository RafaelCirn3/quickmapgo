# Plano de desenvolvimento

## Backlog ordenado

| Etapa | Entrega | Dependência | Critério de saída |
| --- | --- | --- | --- |
| E0 | Documentação inicial | Nenhuma | Escopo, requisitos, modelos e decisões versionados |
| E1 | Prova USB/Wi-Fi e captura de eventos | E0 | Matriz preenchida; repetição de clique e clear verificados |
| E2 | Domínio, gateway e adaptador falso | E0 | Validação, estados e erros testados sem hardware |
| E3 | Interface Streamlit/mapa | E2 + evento validado em E1 | Clique único, marcador, status e demonstração aprovados em testes |
| E4 | Adaptador real | E1 físico + E2 | Conexão, envio e clear nos dois transportes |
| E5 | Integração e tratamento de falhas | E3 + E4 | Critérios RF/RNF essenciais atendidos |
| E6 | Guia Windows e entrega do MVP | E5 | Instalação reproduzível e matriz atualizada |

Sem prazo fechado antes da prova física.

## Tarefas iniciais

- [ ] Registrar ambiente real e versões.
- [ ] Validar USB: descoberta, autorização, set e clear.
- [ ] Validar Wi-Fi sem cabo após pareamento.
- [ ] Verificar evento streamlit-folium: rerun, zoom e clique repetido na mesma coordenada.
- [ ] Fixar dependências compatíveis e escolher integração API/CLI no adaptador.
- [x] Implementar modelos e gateway falso.
- [x] Implementar interface inicial com processamento de evento único.
- [ ] Validar o adaptador experimental com hardware; bloqueio e timeout já implementados.
- [ ] Executar matriz de testes e documentar limites observados.

## Definition of Ready

Tarefa possui requisito vinculado, comportamento esperado, dependências e forma de validação. Integração real precisa de ambiente disponível e evidência da operação correspondente.

## Definition of Done

Critérios da tarefa demonstrados; testes pertinentes executados; erros relevantes tratados; documentação coerente; nenhum dado privado versionado. Tarefas de integração não ficam concluídas apenas com mock. MVP não fica concluído sem USB e Wi-Fi.

## Estado atual

E0 concluída. E2 e E3 implementadas em versão inicial, com validação descrita no relatório. E4 tem adaptador experimental que deve ser validado fisicamente; não está concluída. E1 continua pendente para hardware. E5/E6 têm base de testes, Docker e guia, mas o MVP depende da matriz USB/Wi-Fi real.
