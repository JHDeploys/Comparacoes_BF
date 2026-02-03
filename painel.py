import pandas as pd
import streamlit as st

# ===============================
# Configuração da página
# ===============================
st.set_page_config(
    page_title="Comparação entre Bases de Dados",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ===============================
# Inicialização do estado
# ===============================
if "comparar" not in st.session_state:
    st.session_state.comparar = False

if "boot" not in st.session_state:
    st.session_state.boot = True
    st.rerun()

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

        st.error("Formato de arquivo não suportado. Envie CSV ou XLSX.")
        return None

    except Exception as e:
        st.error(f"Erro ao ler o arquivo: {e}")
        return None


def comparacao_meses(df_anterior, df_atual, coluna_id):
    try:
        if coluna_id not in df_anterior.columns or coluna_id not in df_atual.columns:
            st.error(f"A coluna '{coluna_id}' não existe em um dos arquivos.")
            return None, None

        anterior = df_anterior[
            ~df_anterior[coluna_id].isin(df_atual[coluna_id])
        ]
        atual = df_atual[
            ~df_atual[coluna_id].isin(df_anterior[coluna_id])
        ]

        return anterior, atual

    except Exception as e:
        st.error(f"Erro na comparação: {e}")
        return None, None


# ===============================
# Cabeçalho
# ===============================
st.title("Comparação entre Bases de Dados")
st.markdown(
    """
    <span style="color:yellow; font-weight:bold; font-size:18px;">
        Assistência Social - Prefeitura de Pedra Branca PB
    </span>
    """,
    unsafe_allow_html=True
)

st.divider()

# ===============================
# Controles (layout fixo)
# ===============================
seletor = st.selectbox(
    "Selecione a Coluna de Comparação",
    ["COD_FAMILIAR", "NOME", "CPF", "NIS"]
)

upload_col1, upload_col2 = st.columns(2)

with upload_col1:
    st.markdown("### Arquivo do Mês Anterior")
    mes_anterior = st.file_uploader(
        "Escolha o Arquivo do Mês Anterior",
        type=["csv", "xlsx"]
    )

with upload_col2:
    st.markdown("### Arquivo do Mês Atual")
    mes_atual = st.file_uploader(
        "Escolha o Arquivo do Mês Atual",
        type=["csv", "xlsx"]
    )

if st.button("Realizar Comparação"):
    st.session_state.comparar = True

st.divider()

# ===============================
# Área de resultado (sempre existe)
# ===============================
res_col1, res_col2 = st.columns(2)

with res_col1:
    saidas_container = st.container()

with res_col2:
    entradas_container = st.container()

# ===============================
# Preenchimento condicional
# ===============================
if st.session_state.comparar:

    if mes_anterior is None or mes_atual is None:
        st.warning("Por favor, selecione os dois arquivos para comparar.")

    else:
        df_anterior = ler_arquivo(mes_anterior)
        df_atual = ler_arquivo(mes_atual)

        if df_anterior is not None and df_atual is not None:
            unicos_anterior, unicos_atual = comparacao_meses(
                df_anterior, df_atual, seletor
            )

            if unicos_anterior is not None and unicos_atual is not None:

                with saidas_container:
                    st.markdown(">## **Saíram no Mês Anterior:**")
                    st.markdown(
                        f"<h2 style='color:red;'>{len(unicos_anterior)}</h2>",
                        unsafe_allow_html=True
                    )
                    st.dataframe(unicos_anterior, use_container_width=True)

                    st.download_button(
                        "⬇️ Baixar saídas (CSV)",
                        data=unicos_anterior.to_csv(index=False).encode("utf-8"),
                        file_name="sairam_mes_anterior.csv",
                        mime="text/csv",
                    )

                with entradas_container:
                    st.markdown(">## **Entraram no Mês Atual:**")
                    st.markdown(
                        f"<h2 style='color:green;'>{len(unicos_atual)}</h2>",
                        unsafe_allow_html=True
                    )
                    st.dataframe(unicos_atual, use_container_width=True)

                    st.download_button(
                        "⬇️ Baixar entradas (CSV)",
                        data=unicos_atual.to_csv(index=False).encode("utf-8"),
                        file_name="entraram_mes_atual.csv",
                        mime="text/csv",
                    )
