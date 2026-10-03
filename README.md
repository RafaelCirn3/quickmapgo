# QuickMapGo

Painel local em Python para selecionar coordenadas em um mapa visto de cima e solicitar simulação de localização em um iPhone conectado ao Windows por USB ou Wi-Fi.

**Estado: engenharia de software inicial. Não há aplicação implementada nem compatibilidade comprovada com o iOS 26.6.2 ou com o Pokémon GO.**

## Comportamento pretendido

1. Abrir o painel no navegador do Windows.
2. Selecionar um iPhone e a conexão USB ou Wi-Fi.
3. Clicar no mapa para enviar latitude e longitude.
4. Exibir um marcador da última instrução, suas coordenadas, horário e resultado.
5. Solicitar o encerramento da simulação.

A comunicação envia instruções ao serviço de desenvolvimento do iPhone; não transmite um sinal de satélite GPS. O objetivo de uso informado é o Pokémon GO, cuja aceitação das coordenadas deve ser avaliada separadamente da conexão e do envio.

## Stack definida e candidata

| Componente | Escolha | Situação |
| --- | --- | --- |
| Interface local | Streamlit | Definida pelo usuário |
| Mapa | Folium + streamlit-folium | Candidata; validar eventos de clique |
| Comunicação iOS | pymobiledevice3 | Candidata; validar no aparelho real |
| Execução | Python no Windows, navegador local | Definida |
| Transportes | USB e Wi-Fi | Requisitos obrigatórios do MVP |
| Persistência | Memória durante a execução | Proposta inicial |

Não há necessidade inicial de React, Angular ou FastAPI. Versões serão fixadas após a prova de viabilidade.

## Documentação

- [Visão e escopo](docs/01-visao-escopo.md)
- [Requisitos e critérios de aceite](docs/02-requisitos.md)
- [Casos de uso e interface](docs/03-casos-de-uso-interface.md)
- [Arquitetura](docs/04-arquitetura.md)
- [Modelos e contratos](docs/05-modelos-contratos.md)
- [Viabilidade, riscos e compatibilidade](docs/06-viabilidade-riscos.md)
- [Plano de desenvolvimento](docs/07-plano-desenvolvimento.md)
- [Estratégia de testes](docs/08-testes.md)
- [Decisões de arquitetura](docs/adr/0001-aplicacao-local-streamlit.md)
- [Referências técnicas](docs/referencias.md)
- [Contribuição](CONTRIBUTING.md)

## Primeira etapa

Executar a prova de viabilidade descrita em [viabilidade e riscos](docs/06-viabilidade-riscos.md), começando pelo USB e depois pelo Wi-Fi. Registrar evidências antes de implementar o adaptador real.

Ainda não existem `app.py`, dependências fixadas ou instalador. O comando **planejado**, disponível apenas após a implementação, é:

```powershell
python -m streamlit run app.py --server.address 127.0.0.1 --server.port 8501
```

Endereço planejado: http://127.0.0.1:8501. Wi-Fi refere-se à comunicação Windows–iPhone; o painel continua local.

## Histórico

- 02/10/2026 (America/Fortaleza): documentação inicial, requisitos, modelos, decisões e plano de validação.
