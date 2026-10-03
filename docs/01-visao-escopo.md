# Visão e escopo

## Problema e objetivo

Rafael deseja escolher uma posição no mapa pelo computador Windows e enviar ao seu iPhone uma solicitação de simulação de localização. A interface deve ser simples, construída com Streamlit, e indicar onde ocorreu a última instrução.

O cenário informado envolve iOS 26.6.2 e Pokémon GO. Receber a instrução no dispositivo e o aplicativo consumidor utilizar a localização são resultados diferentes. Ambos permanecem sem validação.

## Usuário e ambiente

Um operador local, um computador Windows e um iPhone selecionado por vez. Sem contas de usuário, serviço em nuvem ou operação multiusuário no MVP. O iPhone deve estar autorizado para comunicação com o computador.

## MVP

- Interface Streamlit em português, com porta explícita e configurável.
- Mapa 2D visto de cima com navegação e zoom.
- Seleção de dispositivo e transporte.
- Conexão por USB e por Wi-Fi, com pré-requisitos documentados.
- Clique no mapa dispara uma instrução quando a conexão estiver pronta.
- Marcador da última tentativa de envio, com estado, coordenadas e horário.
- Registro separado da última instrução com retorno de sucesso.
- Encerrar simulação com resultado visível.
- Modo demonstração sem dispositivo para desenvolver e verificar a interface.

## Fora do escopo inicial

Bluetooth, rotas e movimento contínuo, joystick, automação do jogo, cliente modificado, mecanismos para ocultar a simulação, jailbreak, múltiplos iPhones simultâneos, histórico permanente, hospedagem pública e aplicativo mobile próprio.

## Sucesso do projeto

O MVP só será considerado completo quando os critérios funcionais passarem nos dois transportes no ambiente registrado. A aceitação pelo Pokémon GO será uma conclusão adicional com evidência própria, sem ser inferida do sucesso do adaptador.

## Pendências de descoberta

- Versão/edição do Windows, modelo do iPhone e versão/build exata do iOS.
- Drivers, autorização, modo desenvolvedor e túnel necessários ao ambiente.
- Versões compatíveis das bibliotecas e método de encerramento.
- Resultado observado no consumidor de localização.

Essas pendências serão resolvidas na prova de viabilidade, sem alterar os requisitos USB e Wi-Fi silenciosamente.
