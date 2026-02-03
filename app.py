import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Comparação entre Bases de Dados",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ===============================
# Estado
# ===============================
if "comparar" not in st.session_state:
    st.session_state.comparar = False

if "df_saida" not in st.session_state:
    st.session_state.df_saida = None

if "df_entrada" not in st.session_state:
    st.session_state.df_entrada = None

# ===============================
# Funções
# ===============================
def ler_arquivo(arquivo):
    if arquivo is None:
        return None
    try:
        nome = arquivo.name.lower()
        if nome.endswith(".csv"):
            try:
                return pd.read_csv(arquivo, sep=None, engine="python")
            except Exception:
                return pd.read_csv(arquivo, sep=";", encoding="latin1")
        if nome.endswith(".xlsx"):
            return pd.read_excel(arquivo)
    except Exception as e:
        st.error(f"Erro ao ler arquivo: {e}")
    return None


def comparar(df_a, df_b, col):
    if col not in df_a.columns or col not in df_b.columns:
        st.error(f"Coluna {col} não encontrada.")
        return None, None
    return (
        df_a[~df_a[col].isin(df_b[col])],
        df_b[~df_b[col].isin(df_a[col])]
    )

# ===============================
# UI
# ===============================
st.title("Comparação entre Bases de Dados")
st.subheader("Assistência Social - Prefeitura de Pedra Branca PB")
st.divider()

coluna = st.selectbox(
    "Selecione a Coluna de Comparação",
    ["COD_FAMILIAR", "NOME", "CPF", "NIS"]
)

up1, up2 = st.columns(2)

with up1:
    st.markdown("### Arquivo do Mês Anterior")
    arq_ant = st.file_uploader("Arquivo anterior", ["csv", "xlsx"], key="ant")

with up2:
    st.markdown("### Arquivo do Mês Atual")
    arq_atual = st.file_uploader("Arquivo atual", ["csv", "xlsx"], key="atu")

if st.button("Realizar Comparação"):
    if arq_ant and arq_atual:
        df_ant = ler_arquivo(arq_ant)
        df_at = ler_arquivo(arq_atual)

        if df_ant is not None and df_at is not None:
            st.session_state.df_saida, st.session_state.df_entrada = comparar(
                df_ant, df_at, coluna
            )
            st.session_state.comparar = True
    else:
        st.warning("Selecione os dois arquivos.")

st.divider()

# ===============================
# Resultados (sempre existem)
# ===============================
r1, r2 = st.columns(2)

with r1:
    st.markdown("## Saíram no mês anterior")
    qtd_saida = 0 if st.session_state.df_saida is None else len(st.session_state.df_saida)
    st.metric("Quantidade", qtd_saida)

    st.dataframe(
        st.session_state.df_saida if st.session_state.comparar else pd.DataFrame(),
        use_container_width=True
    )

    st.download_button(
        "⬇️ Baixar saídas",
        data=(
            st.session_state.df_saida.to_csv(index=False).encode("utf-8")
            if st.session_state.df_saida is not None
            else b""
        ),
        file_name="sairam_mes_anterior.csv",
        mime="text/csv",
        disabled=st.session_state.df_saida is None
    )

with r2:
    st.markdown("## Entraram no mês atual")
    qtd_ent = 0 if st.session_state.df_entrada is None else len(st.session_state.df_entrada)
    st.metric("Quantidade", qtd_ent)

    st.dataframe(
        st.session_state.df_entrada if st.session_state.comparar else pd.DataFrame(),
        use_container_width=True
    )

    st.download_button(
        "⬇️ Baixar entradas",
        data=(
            st.session_state.df_entrada.to_csv(index=False).encode("utf-8")
            if st.session_state.df_entrada is not None
            else b""
        ),
        file_name="entraram_mes_atual.csv",
        mime="text/csv",
        disabled=st.session_state.df_entrada is None
    )
