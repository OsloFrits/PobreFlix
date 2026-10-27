"""Leitura e preparação dos dados de filmes e séries da Netflix."""

import csv
from pathlib import Path

# Localiza o arquivo CSV na mesma pasta deste programa.
PASTA = Path(__file__).parent
CAMINHO_TITULOS = PASTA / "filmes-series-netflix.csv"


def ler_titulos():
    """Lê os títulos do arquivo CSV e retorna uma lista de dicionários."""
    titulos = []

    try:
        with open(CAMINHO_TITULOS, "r", encoding="utf-8") as arquivo:
            leitor = csv.DictReader(arquivo)

            for linha in leitor:
                titulos.append(linha)

    except FileNotFoundError:
        print("Erro: arquivo filmes-series-netflix.csv não encontrado.")

    except Exception as erro:
        print(f"Erro ao ler o arquivo: {erro}")

    return titulos


def converter_duracao(duracao):
    """Converte a duração em minutos ou temporadas."""
    duracao = duracao.strip()

    if not duracao:
        return 0, 0

    partes = duracao.split()
    numero = int(partes[0])

    if "min" in duracao:
        return numero, 0

    return 0, numero


def converter_tipo(tipo):
    """Converte o tipo original para português."""
    if tipo.strip() == "Movie":
        return "Filme"

    return "Série"


def converter_ano(ano):
    """Converte o ano para número inteiro."""
    if not ano or not ano.strip():
        return 0

    return int(ano)


def preparar_titulos(linhas):
    """Prepara os dados para serem utilizados no dashboard."""
    titulos = []

    for linha in linhas:
        try:
            minutos, temporadas = converter_duracao(
                linha.get("duracao", "")
            )

            titulo = {
                "titulo": linha.get("titulo", ""),
                "tipo": converter_tipo(linha.get("tipo", "")),
                "pais": linha.get("pais", "") or "Não informado",
                "ano": converter_ano(linha.get("ano", "")),
                "classificacao": (
                    linha.get("classificacao", "")
                    or "Não informada"
                ),
                "duracao_texto": linha.get("duracao", ""),
                "minutos": minutos,
                "temporadas": temporadas,
                "generos": linha.get("generos", ""),
                "data_adicao": linha.get("data_adicao", ""),
            }

            titulos.append(titulo)

        except (ValueError, AttributeError) as erro:
            print(f"Título ignorado por erro nos dados: {erro}")

    return titulos


def carregar_titulos():
    """Carrega o CSV e devolve os dados preparados."""
    linhas = ler_titulos()
    return preparar_titulos(linhas)


def calcular_duracao_media_filmes(titulos):
    """Calcula a duração média dos filmes em minutos."""
    soma = 0
    quantidade = 0

    for titulo in titulos:
        if titulo["tipo"] == "Filme" and titulo["minutos"] > 0:
            soma += titulo["minutos"]
            quantidade += 1

    if quantidade == 0:
        return 0

    return soma / quantidade


def contar_series(titulos):
    """Conta a quantidade de séries."""
    contador = 0

    for titulo in titulos:
        if titulo["tipo"] == "Série":
            contador += 1

    return contador


def encontrar_filme_mais_longo(titulos):
    """Encontra o filme com a maior duração."""
    filmes = [
        titulo
        for titulo in titulos
        if titulo["tipo"] == "Filme" and titulo["minutos"] > 0
    ]

    if not filmes:
        return None

    mais_longo = filmes[0]

    for filme in filmes:
        if filme["minutos"] > mais_longo["minutos"]:
            mais_longo = filme

    return mais_longo


if __name__ == "__main__":
    titulos = carregar_titulos()

    print(f"{len(titulos)} títulos carregados.")

    if titulos:
        print("Primeiro título:", titulos[0])
        print(
            "Duração média dos filmes:",
            calcular_duracao_media_filmes(titulos),
            "minutos"
        )
        print("Quantidade de séries:", contar_series(titulos))

        mais_longo = encontrar_filme_mais_longo(titulos)

        if mais_longo:
            print("Filme mais longo:", mais_longo["titulo"])
