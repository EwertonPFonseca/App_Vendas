from pathlib import Path
import streamlit as st
import pandas as pd
from utilidades import leitura_de_dados

st.set_page_config(page_title='Tabelas', layout="wide")

st.markdown("## Tabela Fonte dos Dados")
leitura_de_dados()


df_vendas = st.session_state['dados']['df_vendas']
df_filiais= st.session_state['dados']['df_filiais']
df_produtos =st.session_state['dados']['df_produtos']

st.sidebar.markdown("### Seleção de Tabelas")
tabela_selecioanda= st.sidebar.selectbox('Selecione uma tabela para visualizar:',
                     ['Vendas','Produtos','Filiais'])

def mostrar_tabela_vendas():
    st.sidebar.divider()
    st.sidebar.markdown('### Filtrar tabela')
    colunas_selecionadas = st.sidebar.multiselect('Selecione as colunas:',
                                                  list(df_vendas.columns),
                                                  list(df_vendas.columns))

    col1,col2 = st.sidebar.columns(2)
    filtro_selecionado = col1.selectbox('Filtrar Coluna',list(df_vendas.columns))

    valores_unicos = list(df_vendas[filtro_selecionado].unique())

    valor_filtro = col2.selectbox('Filtrar valor',valores_unicos)



    bt_filtrar = col1.button('Filtrar')
    bt_limpar = col2.button('Limpar')

    if bt_filtrar:
        st.dataframe(df_vendas.loc[df_vendas[filtro_selecionado]==valor_filtro,colunas_selecionadas],height=800)

    elif bt_limpar:
        st.dataframe(df_vendas[colunas_selecionadas],height=800)
    else:
        st.dataframe(df_vendas,height=800)


def mostrar_tabela_produtos():
    st.dataframe(df_produtos)

def mostrar_tabela_filiais():
    st.dataframe(df_filiais)





if tabela_selecioanda == 'Vendas':
    mostrar_tabela_vendas()

elif tabela_selecioanda =='Produtos':
    mostrar_tabela_produtos()

elif tabela_selecioanda =='Filiais':
    mostrar_tabela_filiais()


