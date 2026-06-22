# Grupo 7 - Sumarizador Legislativo

## Introdução

Este é o projeto final de Estruturas de Dados 2 do Grupo 7. O sistema implementa uma sumarização extrativa de transcrições de debates parlamentares baseada em grafos.

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

No Windows, abra um terminal na raiz do projeto.

```powershell
make install
.\venv\Scripts\Activate.ps1
make run
```

O comando `make install` cria a virtual environment `venv` e instala as dependências. A ativação é necessária porque os alvos `run` e `test` usam o comando `python` disponível no terminal.

### Opção 2: Sem Makefile

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
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
