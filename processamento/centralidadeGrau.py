def processarBloco3(grafo, discursos):
    for indice, linha in enumerate(grafo.matrizAdjacencia):
        discursos[indice].relevancia = sum(linha)
