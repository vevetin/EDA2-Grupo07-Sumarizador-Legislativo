# Grupo 7 - Tema C - Sumarizador Legislativo

| Membro | Matrícula |
| --- | --- |
| Caua Araujo dos Santos | 221022490 |
| Enrico Martins Mantoan Zoratto | 222006688 |
| Maria Clara Sena de Lima | 231012281 |
| Paulo Lucca | 170020339 |
| Weverton Rodrigues da Costa Silva | 221022767 |

## Introdução

O projeto tem como objetivo um sistema de sumarização extrativa para debates legislativos, utilizando grafos para identificar automaticamente os discursos mais representativos de uma sessão parlamentar. A arquitetura foi dividida em quatro blocos principais, responsáveis pelo processamento do texto, modelagem do grafo, cálculo de relevância e geração do resumo final.

O processamento é dividido em quatro etapas:

1. **Bloco 1 - Pré-processamento e Tokenização:** limpeza estrutural, separação de orador e frase, tokenização e criação do vocabulário em tabela hash.
2. **Bloco 2 - Modelagem do Grafo Denso (Índice de Jaccard):** construção da matriz de adjacência densa por similaridade de Jaccard.
3. **Bloco 3 - Influência Relacional (Centralidade de Grau):** cálculo da centralidade de grau ponderada de cada frase.
4. **Bloco 4 - Ranqueamento e Geração do Resumo:** seleção do resumo extrativo e geração das saídas JSON e PDF.

Os PDFs de entrada devem ser colocados em `dados/entrada`. Para cada documento, o sistema cria uma pasta correspondente em `dados/saida`, contendo, entre outros arquivos, o vocabulário, a tabela hash, os discursos do grafo, a matriz de adjacência e o resumo extrativo em JSON e PDF.

## Documentação

- [Apresentação Final (PDF)](Grupo07_Sumarizacao_Extrativa.pdf)
- [Apresentação Final (PPTX)](Grupo07_Sumarizacao_Extrativa.pptx)

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

## Saídas

Para um arquivo `dados/entrada/exemplo.pdf`, as saídas são criadas em `dados/saida/exemplo/`.

- `vocabulario.json`: vocabulário e identificadores dos tokens.
- `tabelaHash.txt`: visualização da tabela hash.
- `discursos.json`: frases processadas, tokens e bitsets.
- `grafoDiscursos.json`: vértices válidos e suas pontuações de relevância.
- `matrizAdjacencia.json`: matriz densa com os pesos de Jaccard.
- `resumoExtrativo.json`: frases selecionadas para o resumo.
- `resumoExtrativo.pdf`: resumo extrativo formatado para leitura.
