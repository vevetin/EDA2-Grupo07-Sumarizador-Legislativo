import json
from pathlib import Path


def salvarResultadoTokenizacao(resultado, diretorioSaida):
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


def salvarVisualizacaoHash(tabela, caminhoArquivo):
    caminhoArquivo = Path(caminhoArquivo)
    caminhoArquivo.parent.mkdir(parents=True, exist_ok=True)
    linhas = []
    linhas.append(f"Tabela Hash — {tabela.quantidade} entradas / {tabela.tamanho} slots")
    linhas.append(f"Fator de carga: {tabela.quantidade / tabela.tamanho:.2%}")
    linhas.append("")
    linhas.append(f"{'Índice':<8} {'Status':<10} {'ID':<6} {'Ocorrências':<12} {'Chave':<20} {'Original'}")
    linhas.append("-" * 80)

    for indice, entrada in enumerate(tabela.vetor):
        if entrada is None:
            linhas.append(f"{indice:<8} {'vazio':<10} {'—':<6} {'—':<12} {'—':<20} {'—'}")
        elif entrada is tabela.lapide:
            linhas.append(f"{indice:<8} {'lápide':<10} {'—':<6} {'—':<12} {'—':<20} {'—'}")
        else:
            linhas.append(f"{indice:<8} {'ocupado':<10} {entrada.idPalavra:<6} {entrada.ocorrencias:<12} {entrada.chave:<20} {entrada.original}")

    caminhoArquivo.write_text("\n".join(linhas), encoding="utf-8")
