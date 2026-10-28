"""Funções para gerenciar os títulos da Minha lista."""

PLANEJO = "Planejo assistir"
ASSISTINDO = "Assistindo"
ASSISTIDO = "Assistido"
OPCOES_STATUS = (PLANEJO, ASSISTINDO, ASSISTIDO)


def buscar_status(minha_lista, titulo):
    """Retorna o status do título, ou "" (vazio) se ele não estiver na lista."""
    return minha_lista.get(titulo, "")


def definir_status(minha_lista, titulo, status_escolhido):
    """Adiciona o título ou atualiza seu status."""
    if status_escolhido not in OPCOES_STATUS:
        raise ValueError(f"Status inválido: {status_escolhido}")
    minha_lista[titulo] = status_escolhido


def contar_por_status(minha_lista, status_escolhido):
    """Conta quantos títulos estão no status informado."""
    return sum(
        1 for status_atual in minha_lista.values()
        if status_atual == status_escolhido
    )


def montar_tabela_lista(minha_lista):
    """Converte a lista em linhas para exibição no Streamlit."""
    tabela = []
    for titulo, status_atual in minha_lista.items():
        tabela.append({"Título": titulo, "Status": status_atual})
    return tabela


def remover_da_lista(minha_lista, titulo):
    """Remove o título, se ele estiver na lista."""
    minha_lista.pop(titulo, None)
