Proposta de Projeto: Sumarização Extrativa de Debates Legislativos via Grafos

1. Visão Geral do Projeto

1.1. O Problema e a Área de Aplicação
A área de aplicação escolhida é a política legislativa. O problema que buscamos resolver é a enorme dificuldade técnica e cognitiva em acompanhar, processar e extrair rapidamente os principais argumentos e decisões contidos nas notas taquigráficas e transcrições de debates parlamentares, que costumam ser documentos longos, exaustivos e complexos.

1.2. A Solução Proposta
Desenvolver um software em linguagem nativa capaz de consumir essas transcrições reais e executar uma sumarização extrativa automática. O sistema analisará a força semântica das declarações para identificar, extrair e compilar apenas as frases mais relevantes que sustentam o núcleo do debate, entregando um resumo direto ao usuário.

1.3. Estruturas de Dados Utilizadas
A arquitetura não utiliza bibliotecas prontas de grafos e combina três estruturas fundamentais para alcançar alto desempenho:

- Grafos Densos (Matriz de Adjacência): Estrutura principal para mapear a rede de similaridade entre as frases.
    
- Tabela de Dispersão (Hash Table): Estrutura adicional para tokenização e mapeamento do vocabulário em tempo de busca O(1).
    
- Fila de Prioridades (Heap de Máximo): Estrutura adicional para ordenar as notas e extrair iterativamente o ranqueamento das frases (Top-K).

2. Fluxo de Execução Detalhado (Pipeline do Sistema)
A arquitetura do sumarizador foi modelada em quatro blocos lógicos sequenciais, desenhados para otimizar o processamento de texto e a análise de grafos densos.

Bloco 1: Pré-processamento e Tokenização (Tabela Hash + Bitsets)
Objetivo: Transformar a linguagem natural em matrizes lógicas computáveis.

- Extração e Limpeza Estrutural (Regex): O sistema consome as notas taquigráficas brutas em PDF e utiliza Expressões Regulares (biblioteca nativa re do Python) para realizar o parsing e apagar ruídos institucionais que "enganariam" o cálculo de similaridade. São removidos sumariamente:

    - Cabeçalhos e paginações (ex: "Sessão de: 10/02/2026", "3/54").

    - Títulos de seção em caixa alta (ex: "ORDEM DO DIA").
    
    - Rubricas do taquígrafo (ex: "(Pausa.)").

- Limpeza Textual: O sistema consome as notas taquigráficas reais e utiliza uma biblioteca externa de PLN (spaCy) para remover stopwords (termos irrelevantes) e aplicar a lematização (reduzindo plurais e conjugações verbais à sua raiz).
    
- Mapeamento String-Número (Anti-Overflow): A palavra limpa é convertida em um número inteiro pela Regra de Horner Iterativa. O espalhamento é aplicado a cada iteração multiplicativa (x = (x * 256 + char) % M), garantindo que o limite de memória da máquina não estoure ao processar textos gigantes.
    
- Mapeamento Hash: O valor numérico determina o índice da palavra na Tabela Hash de Endereçamento Aberto.
    - Caso ocorra colisão de índices, o sistema utiliza o Hashing Duplo. A segunda função hash (fhash2) calcula um salto personalizado para encontrar um espaço vazio.
    
    - Para evitar loops infinitos, o tamanho da tabela (M) será um número primo e a função de salto retornará um valor estritamente coprimo e maior que zero.
    
    - Caso exclusões sejam necessárias no vetor, o algoritmo insere Lápides (Tombstones) — marcadores lógicos (ex: -1) que mantêm a trilha de colisões intacta.

- Saída: O vocabulário global é mapeado e cada frase original do debate se transforma em um Bitset (um vetor de zeros e uns), indicando precisamente quais palavras (IDs) ela contém.

Bloco 2: Modelagem do Grafo Denso (Índice de Jaccard)
Objetivo: Construir a rede de relacionamentos semânticos cruzando os dados das frases.

    Definição Teórica: O sistema cria um grafo não direcionado e ponderado, onde cada Vértice (V) é uma frase da sessão parlamentar.
    Análise Combinatória Simétrica: O algoritmo cruza todos os pares possíveis de vértices comparando seus respectivos Bitsets. Através de operações de porta lógica ultrarrápidas (|AND| / |OR|), calcula-se a interseção e união do vocabulário.
    Cálculo do Peso: A relação de similaridade exata gerada pelas portas lógicas forma o Índice de Jaccard, que varia de 0 a 1 e representa o "peso" da aresta entre as duas frases.
    Saída (Matriz de Adjacência): Como em um texto de debate parlamentar quase todas as frases possuem algum nível de conexão vocabular, o projeto gera um grafo altamente conectado. Esses pesos são armazenados em uma Matriz de Adjacência Densa (O(V2)), que possibilita acesso e manipulação imediatos.

Bloco 3: Influência Relacional e Análise Estrutural
Objetivo: Quantificar o peso de importância de cada declaração no ecossistema do debate.

    Cálculo de Centralidade de Grau: O algoritmo navega pelas linhas da Matriz de Adjacência densa gerada no Bloco 2.
    Soma Ponderada: Para um dado vértice (frase), o processador soma os valores numéricos de todas as arestas (Jaccard) incidentes sobre ele.
    Saída: O sistema produz um vetor de notas (scores). Frases com notas mais altas são matematicamente identificadas como os "nós centrais" da sessão — ou seja, as declarações que mais possuem similaridade com o restante do debate e, portanto, representam a essência da pauta.

Bloco 4: Ranqueamento e Extração Top-K (Fila de Prioridades)
Objetivo: Filtrar os vértices vencedores e exibir o resultado legível.

    Estrutura Max-Heap: O vetor de notas desordenado do bloco anterior é inserido em uma Fila de Prioridades (Heap de Máximo), moldada como uma Árvore Binária Completa.
    Ranqueamento Otimizado: Evitamos ordenar a matriz inteira. Para construir o resumo, aplicamos a operação de extração da raiz iterativamente K vezes. A própria propriedade do Heap garante que o elemento extraído da raiz sempre será o de maior prioridade absoluta naquele momento, possuindo um custo logarítmico extremamente eficiente.
    Saída Final: O sistema mapeia os K vértices extraídos de volta para as suas respectivas linhas de texto original. O programa imprime na tela o Resumo Extrativo, contendo apenas o suprassumo do que foi debatido no parlamento.