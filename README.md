# 🎬 PobreFlix

**Membros:** Ana Clara Duarte, Eduardo H. Cardoso, ADD seu nome PF

**Dataset:** filmes-series-netflix.csv — [Netflix Movies and TV Shows (Kaggle)](https://www.kaggle.com/datasets/shivamb/netflix-shows)

**App publicado:** https://...streamlit.app

Dashboard em Python e Streamlit para explorar filmes e séries da Netflix.

## Funcionalidades

- [x] Leitura do CSV
- [x] Conversão das colunas (tipo, duração, ano, data e gêneros)
- [x] Métricas: total de títulos, filmes/séries, duração média e filme mais longo
- [x] Classificação em faixas de duração
- [x] Tabela com nomes de coluna legíveis
- [x] Busca por título (sem diferenciar maiúsculas)
- [x] Filtro por gênero e tipo, com opção "Todos"
- [x] Busca e filtros funcionando juntos
- [x] Mensagem quando nenhum título é encontrado
- [x] Código organizado em funções e módulos
- [ ] App publicado no Streamlit Community Cloud

## Funcionalidade extra

**Minha lista:** na barra lateral, marque um título como *Planejo assistir*, *Assistindo* ou *Assistido*. O status aparece na tabela e a barra lateral conta quantos títulos há em cada um. Feita no módulo `status.py`, com a lista guardada no `st.session_state`.

**Sortear:** sorteia um título entre os resultados da busca e dos filtros.

## Como rodar

```
pip install -r requirements.txt
streamlit run app.py
```
