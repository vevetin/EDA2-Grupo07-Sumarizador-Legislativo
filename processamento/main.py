import argparse
from dataclasses import dataclass
from pathlib import Path

from estruturas.tabelaHash import TabelaHash
from processamento.centralidadeGrau import calcularCentralidadeGrau
from processamento.discurso import Discurso
from processamento.extratorPDF import extrairTextoPdf
from processamento.geradorResumo import gerarResumoPdf, salvarResumoJson, selecionarDiscursosResumo
from processamento.limpezaEstrutural import extrairDiscursosDeTexto
from processamento.modelagemGrafo import construirGrafoSimilaridade, salvarDiscursosGrafo, salvarMatrizAdjacencia
from processamento.processadorPLN import normalizarFrasesEmLote
from processamento.saida import salvarResultadoTokenizacao, salvarVisualizacaoHash

DIRETORIO_ENTRADA_PADRAO = Path("dados/entrada")
DIRETORIO_SAIDA_PADRAO = Path("dados/saida")


@dataclass
class ResultadoTokenizacao:
    vocabulario: TabelaHash
    discursos: list[Discurso]


def _removerDuplicatas(tokens):
    vistos = TabelaHash()
    tokensUnicos = []

    for item in tokens:
        if isinstance(item, tuple):
            chave, original = item
        else:
            chave, original = item, item

        if vistos.buscar(chave) is not None:
            continue
        vistos.inserir(chave, original)
        tokensUnicos.append((chave, original))

    return tokensUnicos


def tokenizarDiscursos(discursos, normalizarFrase=None):
    vocabulario = TabelaHash()
    tokensPorDiscurso = []

    if normalizarFrase is not None:
        for discurso in discursos:
            tokens = _removerDuplicatas(normalizarFrase(discurso.frase))
            tokensPorDiscurso.append(tokens)
    else:
        frases = [discurso.frase for discurso in discursos]
        todosTokens = normalizarFrasesEmLote(frases)
        for tokens in todosTokens:
            tokensPorDiscurso.append(_removerDuplicatas(tokens))

    for discurso, tokens in zip(discursos, tokensPorDiscurso):
        discurso.tokens = [vocabulario.obterId(chave, original) for chave, original in tokens]
        discurso.bitset = 0

        for idPalavra in discurso.tokens:
            discurso.bitset |= 1 << idPalavra

    return ResultadoTokenizacao(vocabulario=vocabulario, discursos=discursos)


def tokenizarPdf(caminhoPdf, normalizarFrase=None):
    texto = extrairTextoPdf(caminhoPdf)
    discursos = extrairDiscursosDeTexto(texto)
    return tokenizarDiscursos(discursos, normalizarFrase=normalizarFrase)



def processarDocumento(caminhoPdf, diretorioSaida):
    """Executa o pipeline completo para um único documento PDF."""
    # Etapa 1: Tokenização e construção de vocabulário
    resultadoTokenizacao = tokenizarPdf(caminhoPdf)
    salvarResultadoTokenizacao(resultadoTokenizacao, diretorioSaida)
    salvarVisualizacaoHash(resultadoTokenizacao.vocabulario, diretorioSaida / "tabelaHash.txt")

    # Etapa 2: Modelagem do grafo de similaridade (Jaccard)
    resultadoGrafo = construirGrafoSimilaridade(resultadoTokenizacao.discursos)
    salvarMatrizAdjacencia(resultadoGrafo, diretorioSaida)

    # Etapa 3: Centralidade de grau e ranking de relevância
    calcularCentralidadeGrau(resultadoGrafo.grafo, resultadoGrafo.discursos)
    salvarDiscursosGrafo(resultadoGrafo, diretorioSaida)

    resultadoResumo = selecionarDiscursosResumo(resultadoGrafo.discursos)
    salvarResumoJson(
        resultadoResumo,
        diretorioSaida / "resumoExtrativo.json",
        caminhoPdf.name,
        len(resultadoTokenizacao.discursos),
    )
    gerarResumoPdf(
        resultadoResumo,
        diretorioSaida / "resumoExtrativo.pdf",
        caminhoPdf.name,
        len(resultadoTokenizacao.discursos),
    )

    return resultadoTokenizacao, resultadoGrafo, resultadoResumo


def _resolverArquivosEntrada(caminhos):
    """Retorna a lista de PDFs: dos argumentos CLI ou por varredura do diretório padrão."""
    if caminhos:
        return [Path(caminho) for caminho in caminhos]

    if not DIRETORIO_ENTRADA_PADRAO.exists():
        print(f"Diretório '{DIRETORIO_ENTRADA_PADRAO}' não encontrado.")
        return []

    pdfs = sorted(DIRETORIO_ENTRADA_PADRAO.glob("*.pdf"))
    if not pdfs:
        print(f"Nenhum PDF encontrado em '{DIRETORIO_ENTRADA_PADRAO}'.")

    return pdfs


def main():
    parser = argparse.ArgumentParser(
        description="Sumarizador Legislativo — Pipeline de processamento de debates parlamentares."
    )
    parser.add_argument(
        "arquivos",
        nargs="*",
        help="Caminhos dos PDFs a processar. Se omitido, processa todos em dados/entrada/.",
    )
    args = parser.parse_args()

    arquivos = _resolverArquivosEntrada(args.arquivos)

    for caminhoPdf in arquivos:
        diretorioSaida = DIRETORIO_SAIDA_PADRAO / caminhoPdf.stem

        print(f"\n{'-' * 20}")
        print(f"Processando: {caminhoPdf.name}")
        print(f"{'-' * 20}")

        resultadoTokenizacao, resultadoGrafo, resultadoResumo = processarDocumento(caminhoPdf, diretorioSaida)

        grafo = resultadoGrafo.grafo
        print(f"Discursos processados: {len(resultadoTokenizacao.discursos)}")
        print(f"Frases selecionadas: {len(resultadoResumo.discursos)}")
        print(f"Matriz de adjacência: {grafo.quantidadeVertices} x {grafo.quantidadeVertices}")
        print(f"Vocabulário: {resultadoTokenizacao.vocabulario.quantidade} termos")
        print(f"Saída: {diretorioSaida}")


if __name__ == "__main__":
    main()

