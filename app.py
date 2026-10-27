"""Dashboard de filmes e séries da Netflix."""

import streamlit as st
import dados

st.set_page_config(
    page_title="PobreFlix",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 PobreFlix")
st.subheader("Filmes e séries da Netflix")

# Carregar os dados
titulos = dados.carregar_titulos()

if not titulos:
    st.error("Não foi possível carregar os títulos.")
else:
    st.success(f"{len(titulos)} títulos carregados!")

    # Estatísticas
    filmes = [t for t in titulos if t["tipo"] == "Filme"]
    series = [t for t in titulos if t["tipo"] == "Série"]

    col1, col2, col3 = st.columns(3)

    col1.metric("Total de títulos", len(titulos))
    col2.metric("Filmes", len(filmes))
    col3.metric("Séries", len(series))

    # Filtro por tipo
    tipo_escolhido = st.selectbox(
        "Escolha o tipo de conteúdo:",
        ["Todos", "Filme", "Série"]
    )

    if tipo_escolhido == "Todos":
        filtrados = titulos
    else:
        filtrados = [
            t for t in titulos
            if t["tipo"] == tipo_escolhido
        ]

    # Mostrar tabela
    tabela = []

    for t in filtrados:
        tabela.append({
            "Título": t["titulo"],
            "Tipo": t["tipo"],
            "Ano": t["ano"],
            "Classificação": t["classificacao"],
            "Duração": t["duracao_texto"],
            "País": t["pais"],
            "Gêneros": t["generos"]
        })

    st.dataframe(tabela, use_container_width=True)

    # Duração média dos filmes
    media = dados.calcular_duracao_media_filmes(titulos)

    st.metric(
        "Duração média dos filmes",
        f"{media:.0f} minutos"
    )