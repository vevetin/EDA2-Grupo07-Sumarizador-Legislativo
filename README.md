# Grupo 7 - Tema C - Sumarizador Legislativo

| Membro | Matrícula |
| --- | --- |
| Enrico Martins Mantoan Zoratto | 222006688 |
| Caua Araujo dos Santos | 221022490 |
| Weverton Rodrigues da Costa Silva | 221022767 |
| Paulo Lucca | 170020339 |
| Maria Clara Sena de Lima | 231012281 |

## Introdução

O projeto tem como objetivo desenvolver um sistema de sumarização extrativa para debates legislativos, utilizando grafos para identificar automaticamente os discursos mais representativos de uma sessão parlamentar. A arquitetura foi dividida em quatro blocos principais, responsáveis pelo processamento do texto, modelagem do grafo, cálculo de relevância e geração do resumo final.

Cada frase válida do debate é representada por um vértice. As relações entre frases são calculadas com o Índice de Jaccard sobre bitsets de tokens, formando um grafo não direcionado e ponderado. A centralidade de grau ponderada identifica as frases mais conectadas; em seguida, uma fila de prioridades seleciona as frases para o resumo, reduzindo redundâncias e preservando a ordem cronológica original.

O processamento é dividido em quatro etapas:

1. Limpeza estrutural, separação de orador e frase, tokenização e criação do vocabulário em tabela hash.
2. Construção da matriz de adjacência densa por similaridade de Jaccard.
3. Cálculo da centralidade de grau ponderada de cada frase.
4. Seleção do resumo extrativo e geração das saídas JSON e PDF.

Os PDFs de entrada devem ser colocados em `dados/entrada`. Para cada documento, o sistema cria uma pasta correspondente em `dados/saida`, contendo, entre outros arquivos, o vocabulário, a tabela hash, os discursos do grafo, a matriz de adjacência e o resumo extrativo em JSON e PDF.

## Requisitos

- Python 3
- Dependências listadas em `requirements.txt`
- GNU Make para usar o `Makefile` (opcional)

## Como Rodar

### Opção 1: Com o Makefile

#### Windows

```powershell
make install
.\venv\Scripts\Activate.ps1
make run
```

O comando `make install` cria a virtual environment `venv` e instala as dependências. A ativação é necessária porque os alvos `run` e `test` usam o comando `python` disponível no terminal.

#### Linux

```bash
make PYTHON=python3 install
source venv/bin/activate
make run
```

### Opção 2: Sem Makefile

#### Windows

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m processamento.main
```

#### Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m processamento.main
```

O comando processa todos os PDFs em `dados/entrada`.

Para processar somente um arquivo:

```powershell
python -m processamento.main dados\entrada\arquivo.pdf
```

## Makefile

O `Makefile` disponibiliza os seguintes alvos:

| Comando | Descrição |
| --- | --- |
| `make install` | Cria a pasta `venv` e instala as dependências de `requirements.txt`. |
| `make run` | Executa o pipeline para todos os PDFs de `dados/entrada`. |
| `make test` | Executa os testes automatizados em `testes/`. |
| `make clean` | Remove `dados/saida`, `.pytest_cache` e pastas `__pycache__`. |
| `make all` | Executa `make install` e `make run`. |

Após ativar a virtual environment, execute os comandos desejados:

```powershell
make test
make clean
make run
```

## Saídas

Para um arquivo `dados/entrada/exemplo.pdf`, as saídas são criadas em `dados/saida/exemplo/`.

- `vocabulario.json`: vocabulário e identificadores dos tokens.
- `tabelaHash.txt`: visualização da tabela hash.
- `discursos.json`: frases processadas, tokens e bitsets.
- `grafoDiscursos.json`: vértices válidos e suas pontuações de relevância.
- `matrizAdjacencia.json`: matriz densa com os pesos de Jaccard.
- `resumoExtrativo.json`: frases selecionadas para o resumo.
- `resumoExtrativo.pdf`: resumo extrativo formatado para leitura.
