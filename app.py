"""PobreFlix: dashboard de filmes e séries da Netflix (app Streamlit)."""

import random

import streamlit as st

import dados
import status


# ---------------------------------------------------------------------------
# Classificação em faixas
# ---------------------------------------------------------------------------

def classificar_duracao(titulo):
    """Classifica um título em uma faixa de duração.

    Filmes usam os minutos e séries usam a quantidade de temporadas.
    """
    if titulo["tipo"] == "Filme":
        if titulo["minutos"] < 90:
            return "Filme curto"
        elif titulo["minutos"] <= 120:
            return "Filme médio"
        else:
            return "Filme longo"
    else:
        if titulo["temporadas"] == 1:
            return "Minissérie"
        elif titulo["temporadas"] <= 3:
            return "Série média"
        else:
            return "Série longa"


# ---------------------------------------------------------------------------
# Tabela
# ---------------------------------------------------------------------------

def montar_tabela(titulos, minha_lista):
    """Prepara as linhas que aparecem na tabela, com nomes de coluna amigáveis.

    A coluna "Minha lista" mostra o status que a pessoa deu para o título.
    """
    tabela = []
    for titulo in titulos:
        if titulo["tipo"] == "Filme":
            duracao = f"{titulo['minutos']} min"
        elif titulo["temporadas"] == 1:
            duracao = "1 temporada"
        else:
            duracao = f"{titulo['temporadas']} temporadas"

        linha = {
            "Título": titulo["titulo"],
            "Minha lista": status.buscar_status(minha_lista, titulo["titulo"]),
            "Tipo": titulo["tipo"],
            "Ano": titulo["ano"],
            "Duração": duracao,
            "Faixa": classificar_duracao(titulo),
            "Classificação": titulo["classificacao"],
            "País": titulo["pais"],
            "Gêneros": ", ".join(titulo["generos"]),
            "Adicionado em": titulo["data_adicao"],
        }
        tabela.append(linha)
    return tabela


# ---------------------------------------------------------------------------
# Busca e filtros
# ---------------------------------------------------------------------------

def buscar_por_titulo(titulos, busca):
    """Devolve só os títulos que contêm o texto buscado (sem diferenciar maiúsculas)."""
    encontrados = []
    for titulo in titulos:
        if busca.lower().strip() in titulo["titulo"].lower():
            encontrados.append(titulo)
    return encontrados


def listar_generos(titulos):
    """Devolve os gêneros que aparecem nos dados, sem repetição e em ordem alfabética."""
    generos = []
    for titulo in titulos:
        for genero in titulo["generos"]:
            if genero not in generos:
                generos.append(genero)
    generos.sort()
    return generos


def filtrar_por_genero(titulos, genero):
    """Devolve só os títulos do gênero escolhido. Com "Todos", devolve todos."""
    if genero == "Todos":
        return titulos

    resultado = []
    for titulo in titulos:
        if genero in titulo["generos"]:
            resultado.append(titulo)
    return resultado


def listar_tipos(titulos):
    """Devolve os tipos que aparecem nos dados ("Filme", "Série"), sem repetição."""
    tipos = []
    for titulo in titulos:
        if titulo["tipo"] not in tipos:
            tipos.append(titulo["tipo"])
    tipos.sort()
    return tipos


def filtrar_por_tipo(titulos, tipo):
    """Devolve só os títulos do tipo escolhido. Com "Todos", devolve todos."""
    if tipo == "Todos":
        return titulos

    resultado = []
    for titulo in titulos:
        if titulo["tipo"] == tipo:
            resultado.append(titulo)
    return resultado


# ---------------------------------------------------------------------------
# Funcionalidade extra: sortear o que assistir
# ---------------------------------------------------------------------------

def sortear_titulo(titulos):
    """Escolhe um título aleatório da lista (ou None se a lista estiver vazia)."""
    if len(titulos) == 0:
        return None
    return random.choice(titulos)


def mostrar_sorteio(encontrados):
    """Mostra o botão de sorteio e o título sorteado entre os resultados atuais."""
    st.subheader("🎲 Não sabe o que assistir?")
    st.caption("Sorteia um título entre os resultados da busca e dos filtros acima.")

    if st.button("Sortear um título"):
        sorteado = sortear_titulo(encontrados)
        if sorteado is None:
            st.warning("Não há títulos para sortear com esses filtros.")
        else:
            st.success(f"**{sorteado['titulo']}**  ({sorteado['tipo']}, {sorteado['ano']})")
            st.write(f"**Duração:** {sorteado['duracao_texto']}  ·  "
                     f"**Classificação:** {sorteado['classificacao']}  ·  "
                     f"**País:** {sorteado['pais']}")
            st.write(f"**Gêneros:** {', '.join(sorteado['generos'])}")


# ---------------------------------------------------------------------------
# Funcionalidade extra: Minha lista (Planejo assistir / Assistindo / Assistido)
# ---------------------------------------------------------------------------

def carregar_minha_lista():
    """Pega a lista guardada na sessão do Streamlit (cria uma vazia na primeira vez).

    O st.session_state guarda valores entre um clique e outro; sem ele,
    a lista seria apagada toda vez que a página atualiza.
    """
    if "minha_lista" not in st.session_state:
        st.session_state["minha_lista"] = {}
    return st.session_state["minha_lista"]


def mostrar_minha_lista(encontrados, minha_lista):
    """Desenha a "Minha lista" na barra lateral: adicionar, trocar status e remover."""
    barra = st.sidebar
    barra.header("📋 Minha lista")

    # Adicionar ou trocar o status (só títulos que passaram pela busca e filtros)
    barra.subheader("Adicionar / trocar status")
    if len(encontrados) == 0:
        barra.info("Nenhum título nos resultados para adicionar.")
    else:
        nomes = []
        for titulo in encontrados:
            nomes.append(titulo["titulo"])

        escolhido = barra.selectbox("Título", nomes)
        status_escolhido = barra.radio("Status", status.OPCOES_STATUS)
        if barra.button("Salvar na lista"):
            status.definir_status(minha_lista, escolhido, status_escolhido)
            barra.success(f"{escolhido} → {status_escolhido}")

    # Contadores por status (depois do botão, para já contarem o título salvo)
    barra.divider()
    col1, col2, col3 = barra.columns(3)
    col1.metric("📌 Planejo", status.contar_por_status(minha_lista, status.PLANEJO))
    col2.metric("▶️ Vendo", status.contar_por_status(minha_lista, status.ASSISTINDO))
    col3.metric("✅ Visto", status.contar_por_status(minha_lista, status.ASSISTIDO))

    # Lista atual e remoção
    if len(minha_lista) == 0:
        barra.caption("Sua lista está vazia.")
    else:
        barra.subheader("Na sua lista")
        barra.dataframe(status.montar_tabela_lista(minha_lista), hide_index=True)

        para_remover = barra.selectbox("Remover título", list(minha_lista.keys()))
        if barra.button("Remover da lista"):
            status.remover_da_lista(minha_lista, para_remover)
            st.rerun()   # atualiza a página para a tabela já sair sem o título


# ---------------------------------------------------------------------------
# Página
# ---------------------------------------------------------------------------

def main():
    st.set_page_config(page_title="PobreFlix", page_icon="🎬", layout="wide")
    st.title("🎬 PobreFlix")
    st.caption("Filmes e séries da Netflix")

    titulos = dados.carregar_titulos()
    if len(titulos) == 0:
        st.error("Não foi possível carregar os títulos.")
        return

    # Métricas
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total de títulos", len(titulos))
    col2.metric("Filmes / Séries",
                f"{dados.contar_por_tipo(titulos, 'Filme')} / {dados.contar_por_tipo(titulos, 'Série')}")

    media = dados.calcular_duracao_media_filmes(titulos)
    col3.metric("Duração média dos filmes", f"{media:.0f} min")

    mais_longo = dados.encontrar_filme_mais_longo(titulos)
    col4.metric("Filme mais longo", f"{mais_longo['minutos']} min")
    col4.caption(mais_longo["titulo"])

    # Busca e filtros (funcionam juntos)
    col_busca, col_tipo, col_genero = st.columns([2, 1, 1])
    busca = col_busca.text_input("🔎 Buscar pelo título")
    tipo = col_tipo.selectbox("Tipo", ["Todos"] + listar_tipos(titulos))
    genero = col_genero.selectbox("Gênero", ["Todos"] + listar_generos(titulos))

    encontrados = filtrar_por_tipo(titulos, tipo)
    encontrados = filtrar_por_genero(encontrados, genero)
    encontrados = buscar_por_titulo(encontrados, busca)

    # A barra lateral vem antes da tabela para a tabela já mostrar o status novo
    minha_lista = carregar_minha_lista()
    mostrar_minha_lista(encontrados, minha_lista)

    if len(encontrados) == 0:
        st.warning("Nenhum título encontrado.")
    else:
        st.write(f"Títulos encontrados: {len(encontrados)}")
        st.dataframe(montar_tabela(encontrados, minha_lista))

    mostrar_sorteio(encontrados)


if __name__ == "__main__":
    main()
