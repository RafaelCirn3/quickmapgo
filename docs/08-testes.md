# Estratégia de testes

Não há testes executáveis nesta etapa documental. Este plano orienta a implementação.

| Teste | Tipo | Requisitos | Resultado esperado |
| --- | --- | --- | --- |
| Coordenadas limítrofes, inválidas, NaN/inf | Unitário | RF11 | Aceitar limites; rejeitar demais |
| Rerun do mesmo evento | Unitário/integração UI | RF06, RNF06 | Um único envio |
| Novo evento na mesma coordenada | Integração UI | RF06 | Nova tentativa permitida |
| Zoom/arraste | Integração UI | RF02, RNF06 | Nenhum envio |
| Última tentativa falha após sucesso | Unitário | RF07, RF08 | Marcador falho; sucesso anterior preservado |
| Timeout após despacho | Unitário com falso | RNF05 | Resultado incerto; sem retry |
| Set concorrente com clear/segunda aba | Integração | RNF04 | Apenas uma operação ativa |
| Dispositivo ausente/não autorizado | Integração/manual | RF03–RF05 | Erro compreensível; nenhum envio |
| USB conecta/set/clear | Manual com hardware | RF04, RF06, RF09 | Evidência de cada operação |
| Wi-Fi sem cabo conecta/set/clear | Manual com hardware | RF05, RF06, RF09 | Evidência independente de USB |
| Desconectar rede/cabo e reconectar | Manual com hardware | RF10 | Bloqueio; não reaplicar posição automaticamente |
| Porta ocupada e binding local | Manual | RF01, RNF02 | Diagnóstico; servidor não exposto à rede |
| Tiles indisponíveis | Manual UI | RNF07 | Estado/controles continuam utilizáveis |
| Consumidor de localização | Manual separado | Objetivo de uso | Registrar observação, sem inferir pelo retorno do gateway |

Testes do domínio e serviços podem usar pytest; ferramentas de interface serão escolhidas na implementação. Não depender de hardware para todos os testes automatizados.

## Evidência mínima

Versões, transporte, procedimento, expectativa, observação, resultado aprovado/reprovado/inconclusivo e diagnóstico sanitizado. Identificar se a conclusão veio de mock, serviço real ou aplicativo consumidor.

Uma captura de marcador no mapa não comprova que a localização foi aplicada ao iPhone. Uma operação sent não comprova que o consumidor a aceitou. Clear com retorno positivo deve ser acompanhado de observação ao validar a recuperação.

## Regressão

Após mudar biblioteca, transporte, deduplicação ou ciclo de vida, repetir os cenários afetados. Mudanças apenas em documentação exigem revisão de links, consistência e requisitos, sem criar testes que espelhem texto.
