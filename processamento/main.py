import json
from dataclasses import dataclass
from pathlib import Path

from estruturas.tabelaHash import TabelaHash
from processamento.discurso import DiscursoProcessado
from processamento.extratorPDF import extrairTextoPdf
from processamento.limpezaEstrutural import extrairDiscursosDeTexto
from processamento.processadorPLN import normalizarFrasesEmLote


@dataclass
class ResultadoBloco1:
    vocabulario: TabelaHash
    discursos: list[DiscursoProcessado]


def processarBloco1(discursos, normalizarFrase=None):
    vocabulario = TabelaHash()
    tokensPorDiscurso = []

    if normalizarFrase is not None:
        # Modo individual
        for discurso in discursos:
            tokens = _removerDuplicatas(normalizarFrase(discurso.frase))
            tokensPorDiscurso.append(tokens)
    else:
        # Modo lote
        frases = [discurso.frase for discurso in discursos]
        todosTokens = normalizarFrasesEmLote(frases)
        for tokens in todosTokens:
            tokensPorDiscurso.append(_removerDuplicatas(tokens))

    discursosProcessados = []

    for discurso, tokens in zip(discursos, tokensPorDiscurso):
        idsTokens = [vocabulario.obterId(token) for token in tokens]
        bitset = 0

        for idPalavra in idsTokens:
            bitset |= 1 << idPalavra

        discursosProcessados.append(
            DiscursoProcessado(
                orador=discurso.orador,
                frase=discurso.frase,
                tokens=idsTokens,
                bitset=bitset,
            )
        )

    return ResultadoBloco1(vocabulario=vocabulario, discursos=discursosProcessados)


def processarPdfBloco1(caminhoPdf, normalizarFrase=None):
    texto = extrairTextoPdf(caminhoPdf)
    discursos = extrairDiscursosDeTexto(texto)
    return processarBloco1(discursos, normalizarFrase=normalizarFrase)


def salvarResultadoBloco1(resultado, diretorioSaida):
    diretorioSaida = Path(diretorioSaida)
    diretorioSaida.mkdir(parents=True, exist_ok=True)

    caminhoVocabulario = diretorioSaida / "vocabulario.json"
    vocabulario = resultado.vocabulario.listarPalavras()
    caminhoVocabulario.write_text(
        json.dumps(vocabulario, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    caminhoDiscursos = diretorioSaida / "discursos.json"
    discursos = [
        {
            "orador": discurso.orador,
            "frase": discurso.frase,
            "tokens": discurso.tokens,
            "bitset": bin(discurso.bitset),
        }
        for discurso in resultado.discursos
    ]
    caminhoDiscursos.write_text(
        json.dumps(discursos, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def _removerDuplicatas(tokens):
    vistos = TabelaHash()
    tokensUnicos = []

    for token in tokens:
        if vistos.buscar(token) is not None:
            continue
        vistos.inserir(token)
        tokensUnicos.append(token)

    return tokensUnicos


def salvarVisualizacaoHash(tabela, caminhoArquivo):
    caminhoArquivo = Path(caminhoArquivo)
    caminhoArquivo.parent.mkdir(parents=True, exist_ok=True)
    linhas = []
    linhas.append(f"Tabela Hash — {tabela.quantidade} entradas / {tabela.tamanho} slots")
    linhas.append(f"Fator de carga: {tabela.quantidade / tabela.tamanho:.2%}")
    linhas.append("")
    linhas.append(f"{'Índice':<8} {'Status':<10} {'ID':<6} {'Chave'}")
    linhas.append("-" * 50)

    for indice, entrada in enumerate(tabela.vetor):
        if entrada is None:
            linhas.append(f"{indice:<8} {'vazio':<10} {'—':<6} {'—'}")
        elif entrada is tabela.lapide:
            linhas.append(f"{indice:<8} {'lápide':<10} {'—':<6} {'—'}")
        else:
            linhas.append(f"{indice:<8} {'ocupado':<10} {entrada.idPalavra:<6} {entrada.chave}")

    caminhoArquivo.write_text("\n".join(linhas), encoding="utf-8")


def main():
    caminhoEntrada = Path("dados/entrada/entrada1.pdf")
    diretorioSaida = Path("dados/saida")
    resultado = processarPdfBloco1(caminhoEntrada)
    salvarResultadoBloco1(resultado, diretorioSaida)
    salvarVisualizacaoHash(resultado.vocabulario, diretorioSaida / "tabelaHash.txt")
    print(f"Discursos processados: {len(resultado.discursos)}")
    print(f"Vocabulário: {resultado.vocabulario.quantidade} termos")
    print(f"Saída: {diretorioSaida}")


if __name__ == "__main__":
    main()
