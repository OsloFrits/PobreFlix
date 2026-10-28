"""Leitura e preparação dos dados de filmes e séries da Netflix."""

import csv
from pathlib import Path

# Pasta onde este arquivo .py está. Assim o programa encontra o CSV
# mesmo quando é executado a partir de outra pasta (como no Streamlit Cloud).
PASTA = Path(__file__).parent
CAMINHO_TITULOS = PASTA / "filmes-series-netflix.csv"

# Meses em inglês (como vêm no CSV) -> número do mês
MESES = {
    "January": 1, "February": 2, "March": 3, "April": 4,
    "May": 5, "June": 6, "July": 7, "August": 8,
    "September": 9, "October": 10, "November": 11, "December": 12,
}


# ---------------------------------------------------------------------------
# Leitura do CSV
# ---------------------------------------------------------------------------

def ler_titulos():
    """Lê o CSV e devolve uma lista de dicionários.

    Os valores vêm do jeito que estão no arquivo, ou seja, como texto:
    {"titulo": "3%", "tipo": "TV Show", "duracao": "4 Seasons", ...}
    """
    titulos = []
    try:
        with open(CAMINHO_TITULOS, "r", encoding="utf-8") as arquivo:
            leitor = csv.DictReader(arquivo)
            for linha in leitor:
                titulos.append(linha)
    except FileNotFoundError:
        print("O arquivo filmes-series-netflix.csv não foi encontrado")
    except Exception as erro:
        print("Algum erro aconteceu na leitura do arquivo", erro)

    return titulos


# ---------------------------------------------------------------------------
# Conversões (texto do CSV -> valores que dá para usar nos cálculos)
# ---------------------------------------------------------------------------

def converter_tipo(tipo):
    """Traduz o tipo: "Movie" -> "Filme", "TV Show" -> "Série"."""
    if tipo.strip() == "Movie":
        return "Filme"
    return "Série"


def converter_duracao(duracao):
    """Separa o número da unidade e devolve (minutos, temporadas).

    "95 min"    -> (95, 0)
    "4 Seasons" -> (0, 4)
    "1 Season"  -> (0, 1)
    """
    duracao = duracao.strip()
    if duracao == "":
        return 0, 0

    numero = int(duracao.split()[0])
    if "min" in duracao:
        return numero, 0
    return 0, numero


def converter_ano(ano):
    """Converte o ano de texto para número: "2020" -> 2020."""
    if ano.strip() == "":
        return 0
    return int(ano)


def converter_data(data):
    """Converte a data em inglês para o formato brasileiro.

    "August 14, 2020" -> "14/08/2020"
    """
    data = data.strip()
    if data == "":
        return ""

    partes = data.replace(",", "").split()   # ["August", "14", "2020"]
    mes = MESES[partes[0]]
    dia = int(partes[1])
    ano = int(partes[2])
    return f"{dia:02d}/{mes:02d}/{ano}"


def converter_generos(generos):
    """Transforma o texto dos gêneros em uma lista.

    "Dramas, International Movies" -> ["Dramas", "International Movies"]
    """
    lista = []
    for genero in generos.split(","):
        genero = genero.strip()
        if genero != "":
            lista.append(genero)
    return lista


def preparar_titulos(linhas):
    """Recebe as linhas lidas do CSV e devolve os títulos já convertidos."""
    titulos = []
    for linha in linhas:
        try:
            minutos, temporadas = converter_duracao(linha["duracao"])
            titulo = {
                "titulo": linha["titulo"],
                "tipo": converter_tipo(linha["tipo"]),
                "pais": linha["pais"] or "Não informado",
                "ano": converter_ano(linha["ano"]),
                "data_adicao": converter_data(linha["data_adicao"]),
                "classificacao": linha["classificacao"] or "Não informada",
                "duracao_texto": linha["duracao"],
                "minutos": minutos,
                "temporadas": temporadas,
                "generos": converter_generos(linha["generos"]),
            }
            titulos.append(titulo)
        except (ValueError, KeyError) as erro:
            print("Título ignorado por erro nos dados:", erro)

    return titulos


def carregar_titulos():
    """Lê o CSV e já devolve os títulos prontos para usar."""
    return preparar_titulos(ler_titulos())


# ---------------------------------------------------------------------------
# Métricas
# ---------------------------------------------------------------------------

def contar_por_tipo(titulos, tipo):
    """Conta quantos títulos são do tipo pedido ("Filme" ou "Série")."""
    contador = 0
    for titulo in titulos:
        if titulo["tipo"] == tipo:
            contador += 1
    return contador


def calcular_duracao_media_filmes(titulos):
    """Soma a duração (em minutos) de todos os filmes e divide pela quantidade."""
    soma = 0
    quantidade = 0
    for titulo in titulos:
        if titulo["tipo"] == "Filme" and titulo["minutos"] > 0:
            soma += titulo["minutos"]
            quantidade += 1

    if quantidade == 0:
        return 0
    return soma / quantidade


def encontrar_filme_mais_longo(titulos):
    """Devolve o filme com mais minutos (ou None se não houver filmes)."""
    mais_longo = None
    for titulo in titulos:
        if titulo["tipo"] == "Filme":
            if mais_longo is None or titulo["minutos"] > mais_longo["minutos"]:
                mais_longo = titulo
    return mais_longo


def encontrar_serie_mais_longa(titulos):
    """Devolve a série com mais temporadas (ou None se não houver séries)."""
    mais_longa = None
    for titulo in titulos:
        if titulo["tipo"] == "Série":
            if mais_longa is None or titulo["temporadas"] > mais_longa["temporadas"]:
                mais_longa = titulo
    return mais_longa


if __name__ == "__main__":
    titulos = carregar_titulos()
    print(f"{len(titulos)} títulos carregados")
    print("Primeiro título:", titulos[0])
    print("Filmes:", contar_por_tipo(titulos, "Filme"))
    print("Séries:", contar_por_tipo(titulos, "Série"))
    print(f"Duração média dos filmes: {calcular_duracao_media_filmes(titulos):.0f} min")
    print("Filme mais longo:", encontrar_filme_mais_longo(titulos)["titulo"])
    print("Série mais longa:", encontrar_serie_mais_longa(titulos)["titulo"])
