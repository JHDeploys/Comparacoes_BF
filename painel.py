import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Comparação entre Bases de Dados",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)
def ler_arquivo(arquivo):
    try:
        if arquivo is None:
            return None
        
        nome = arquivo.name.lower()
        
        if nome.endswith('.csv'):
            try:
                return pd.read_csv(arquivo, sep=None, engine='python')
            except Exception:
                return pd.read_csv(arquivo, sep=';', encoding='latin1')
        
        elif nome.endswith('.xlsx'):
            return pd.read_excel(arquivo)
        
        else:
            st.error("Formato de arquivo não suportado. Por favor, envie um arquivo CSV ou XLSX.")
            return None
        
    except Exception as e:
        st.error(f"Erro ao ler o arquivo: {e}")
        return None


def comparacao_meses(df_anterior, df_atual, coluna_id):
    try:
        if coluna_id not in df_anterior.columns or coluna_id not in df_atual.columns:
            st.error(f"A coluna '{coluna_id}' não existe em um dos arquivos.")
            return None, None

        anterior = df_anterior[~df_anterior[coluna_id].isin(df_atual[coluna_id])]
        atual = df_atual[~df_atual[coluna_id].isin(df_anterior[coluna_id])]
        
        return anterior, atual
    
    except Exception as e:
        st.error(f"Erro na comparação dos dados: {e}")
        return None, None



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

seletor = st.selectbox("Selecione a Coluna de Comparação", ["COD_FAMILIAR", "NOME", "CPF", "NIS"])
col1, col2 = st.columns(2)
with col1:
    st.markdown('### Arquivo do Mês Anterior')
    mes_anterior = st.file_uploader("Escolha o Arquivo do Mês Anterior", type=["csv", "xlsx"])
with col2:
    st.markdown('### Arquivo do Mês Atual')
    mes_atual = st.file_uploader("Escolha o Arquivo do Mês Atual", type=["csv", "xlsx"])

col1, col2, col3 = st.columns([1,6,1])
with col1:
    st.write("")
with col2:
    comparar = st.button("Realizar Comparação")
with col3:
    st.write("")
st.divider()

if comparar:
    if mes_anterior is None or mes_atual is None:
        st.warning("Por favor, selecione os dois arquivos para comparar.")
    else:
        df_anterior = ler_arquivo(mes_anterior)
        df_atual = ler_arquivo(mes_atual)

        if df_anterior is not None and df_atual is not None:
            unicos_anterior, unicos_atual = comparacao_meses(df_anterior, df_atual, seletor)

            if unicos_anterior is not None and unicos_atual is not None:
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown(">## **Saíram no Mês Anterior:**")
                    st.markdown( f"<h2 style='color:red;'>{len(unicos_anterior)}</h3>", unsafe_allow_html=True)
                    st.dataframe(unicos_anterior)

                    csv1 = unicos_anterior.to_csv(index=False).encode("utf-8")
                    st.download_button(
                        "⬇️ Baixar saídas (CSV)",
                        data=csv1,
                        file_name="sairam_mes_anterior.csv",
                        mime="text/csv",
                    )

                with col2:
                    st.markdown(">## **Entraram no Mês Atual:**")
                    st.markdown( f"<h2 style='color:green;'>{len(unicos_atual)}</h3>", unsafe_allow_html=True)
                    st.dataframe(unicos_atual)

                    csv2 = unicos_atual.to_csv(index=False).encode("utf-8")
                    st.download_button(
                        "⬇️ Baixar entradas (CSV)",
                        data=csv2,
                        file_name="entraram_mes_atual.csv",
                        mime="text/csv",
                    )
