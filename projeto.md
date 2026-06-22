# Status Atual do Projeto – Sumarização Extrativa de Debates Legislativos

## Visão Geral

O projeto tem como objetivo desenvolver um sistema de sumarização extrativa para debates legislativos, utilizando grafos para identificar automaticamente os discursos mais representativos de uma sessão parlamentar. A arquitetura foi dividida em quatro blocos principais, responsáveis pelo processamento do texto, modelagem do grafo, cálculo de relevância e geração do resumo final.

## Bloco 1 – Pré-processamento e Tokenização

### Objetivo

Transformar as transcrições parlamentares em uma representação computacional adequada para análise.

### Implementação

* Limpeza estrutural das notas taquigráficas.
* Remoção de ruídos textuais.
* Tokenização e normalização dos termos.
* Construção do vocabulário utilizando tabela hash.
* Representação dos discursos por meio de bitsets.

### Status

**Concluído**

Os discursos já são convertidos para uma estrutura eficiente de armazenamento e consulta, servindo como entrada para as etapas posteriores.

---

## Bloco 2 – Construção do Grafo de Similaridade

### Objetivo

Modelar as relações semânticas entre os discursos do debate.

### Implementação

* Comparação entre os bitsets dos discursos.
* Cálculo do Índice de Jaccard para cada par de discursos.
* Construção da matriz de adjacência ponderada.
* Armazenamento das similaridades em um grafo não direcionado.

### Status

**Concluído**

O sistema já é capaz de gerar a rede de similaridade entre os discursos, produzindo a estrutura necessária para os cálculos de relevância.

---

## Bloco 3 – Análise Estrutural e Cálculo de Relevância

### Objetivo

Identificar quais discursos possuem maior importância dentro da rede construída.

### Implementação

A relevância de cada discurso é calculada por meio da centralidade de grau ponderada. Para cada vértice do grafo, são somados os pesos das arestas incidentes, produzindo uma nota de relevância.

### Alteração de Modelagem

Inicialmente, o resultado dessa etapa seria armazenado em uma lista separada contendo apenas os scores dos discursos.

Entretanto, foi identificada uma melhoria na modelagem: adicionar um atributo de relevância diretamente à classe que representa cada discurso.

Com essa alteração:

* Cada objeto armazenará seu próprio score.
* A associação entre discurso e nota torna-se direta.
* Reduz-se a dependência de estruturas paralelas.
* Facilita-se a implementação do ranqueamento no Bloco 4.

### Status

**Concluído**

---

## Bloco 4 – Ranqueamento e Geração do Resumo

### Objetivo

Selecionar os discursos mais relevantes de forma proporcional ao tamanho do documento, filtrando redundâncias e preservando a cronologia do debate para compor um resumo extrativo coeso.

### Implementação
* Definição Dinâmica de Limite: Cálculo do valor de "K" (quantidade de extrações) baseado em uma porcentagem do total de discursos.
* Ranqueamento: Inserção dos discursos (e seus respectivos scores) em uma fila de prioridades (Max-Heap).
* Extração com Filtro Anti-Redundância: Remoção iterativa dos discursos de maior relevância do topo da Max-Heap, validando-os através de uma operação lógica `AND` com o "Bitset do Resumo" para descartar frases repetitivas. Discursos aceitos atualizam o filtro com uma operação `OR`.
* Reordenação Temporal: Organização dos discursos aprovados de acordo com sua posição original no texto base.
* Recuperação e Saída: Recuperação do texto original associado a cada discurso selecionado e geração do resumo final.

### Status
**Concluído**

#### Decisões de Arquitetura e Implementação (Bloco 4)

Com o objetivo de solucionar desafios de redundância, variação de tamanho e coesão textual, as seguintes decisões foram consolidadas e implementadas:

##### 1. Geração do Resumo e Variação entre Documentos (K Dinâmico)
Para lidar com documentos de tamanhos variados sem gerar resumos insuficientes ou excessivos.
* **Implementação:** A quantidade de frases ("K") é calculada dinamicamente, sendo 8% do total de discursos válidos processados, contendo limites inferiores e superiores (piso de 12 e teto de 60 frases) para garantir um tamanho coerente do texto gerado.

##### 2. Redundância de Informações (Filtro por Bitsets)
Para evitar que o resumo final contenha frases repetitivas de alta relevância.
* **Implementação:** Foi criado um "Bitset do Resumo". Durante a extração da Fila de Prioridade, calcula-se a taxa de intersecção (`AND` lógico) dos tokens da frase contra os tokens já presentes no resumo. Se a redundância ultrapassar o limiar de 70%, o discurso é descartado. Caso passe, seus tokens são adicionados ao resumo via `OR` lógico, dispensando novas consultas em matrizes.

##### 3. Organização da Saída (Ordem Cronológica)
Para preservar a lógica original do debate e formato de "Perguntas e Respostas".
* **Implementação:** Os discursos escolhidos para o Top-K são reordenados utilizando um atributo `indiceOriginal` de cada frase, que guarda a posição no documento nativo, montando um PDF fluido, coerente e com os diálogos agrupados adequadamente pelo orador.