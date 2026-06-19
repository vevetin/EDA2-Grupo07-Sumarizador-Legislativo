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

### Implementação Prevista

A relevância de cada discurso será calculada por meio da centralidade de grau ponderada. Para cada vértice do grafo, serão somados os pesos das arestas incidentes, produzindo uma nota de relevância.

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

Selecionar os discursos mais relevantes para compor o resumo extrativo.

### Implementação Prevista

* Inserção dos discursos em uma fila de prioridades (Max-Heap).
* Extração dos K discursos de maior relevância.
* Recuperação do texto original associado a cada discurso selecionado.
* Geração do resumo final.

### Status

**Não iniciado**

A implementação deste bloco começará após a conclusão do Bloco 3.

---

## Situação Atual

### Concluído

* Bloco 1 – Pré-processamento e Tokenização.
* Bloco 2 – Construção do Grafo de Similaridade.
* Bloco 3 – Análise Estrutural e Cálculo de Relevância.

### Em andamento

* Bloco 4 – Ranqueamento e Geração do Resumo.

### Próximos Passos

1. Implementar a Max-Heap para ranqueamento.
2. Desenvolver a extração Top-K.
3. Integrar todos os blocos e realizar testes com transcrições reais.

## Dúvidas para Discussão com a Equipe

### Geração do Resumo

Após o cálculo das notas de relevância e o ranqueamento dos discursos, como será definido o conjunto de discursos que comporá o resumo final?

Algumas possibilidades levantadas até o momento são:

* Selecionar os K discursos mais relevantes;
* Selecionar uma porcentagem dos discursos do documento;
* Utilizar algum limiar mínimo de relevância.

### Variação entre Documentos

Como o sistema deve se comportar diante de documentos com tamanhos muito diferentes?

Um mesmo critério de seleção funcionará adequadamente para debates curtos e longos ou será necessário adaptar o tamanho do resumo de acordo com o documento analisado?

### Redundância de Informações

Discursos muito semelhantes podem receber notas de relevância próximas. Será necessário implementar algum mecanismo para evitar que informações repetidas apareçam no resumo final?

### Organização da Saída

Após selecionar os discursos mais relevantes, eles devem ser exibidos em ordem de relevância ou reordenados conforme sua posição original no debate para preservar a sequência lógica da discussão?
