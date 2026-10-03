# Contribuição

## Fluxo proposto

Usar main como referência estável; trabalho futuro em branches docs/, feat/ ou fix/, com PR de escopo pequeno. A documentação inicial pode ser gravada diretamente em main conforme solicitação de preparação. Proteções de branch não foram configuradas nesta etapa.

Antes de implementar hardware, consultar a prova de viabilidade. Não substituir Streamlit nem remover USB/Wi-Fi sem atualizar decisão e requisitos.

## Convenções

Documentação em português. IDs RF/RNF para rastreabilidade. Commits como docs: ..., feat: ... e fix: .... Novas decisões relevantes recebem ADR em docs/adr/. Separar instruções previstas de comandos efetivamente disponíveis.

## Revisão

Verificar links relativos, termos de estado e consistência do escopo. Implementações precisam dos testes pertinentes ao comportamento. Registrar separadamente teste falso e teste físico. Não commitar dados de pareamento, logs privados ou identificadores reais. Nenhuma licença de software foi escolhida por esta preparação.
