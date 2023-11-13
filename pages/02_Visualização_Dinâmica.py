from pathlib import Path
import streamlit as st
import pandas as pd
from utilidades import leitura_de_dados,COMISSAO



st.set_page_config(page_title='Visualização Dinâmica', layout="wide")

st.markdown("## Visualização Tabela Dinâmica")
leitura_de_dados()
# passando uma lista de colunas que vamos usar na dinâmica

COLUNAS_ANALISE = ['filial','vendedor','produto','cliente_genero','forma_pagamento']
COLUNAS_VALOR = ['preco','comissao']
FUNCOES_AGG = {'soma':'sum','contagem':'count'}


df_vendas = st.session_state['dados']['df_vendas']
df_filiais= st.session_state['dados']['df_filiais']
df_produtos =st.session_state['dados']['df_produtos']

df_produtos = df_produtos.rename(columns={'nome':'produto'})

#para fazer o merge, é melhor dar um reset no índice da tabela vendas

df_vendas = df_vendas.reset_index()

#merge tabela vendas com produtos

df_vendas = pd.merge(left= df_vendas,
                     right= df_produtos[['produto','preco']],
                     on='produto',
                     how='left')

#retorna a coluna de data como índice
df_vendas.set_index('data')

#adicionar valor comissão na tabela vendas
df_vendas['comissao']= df_vendas['preco']* COMISSAO


#criando os campos de seleção na sidebar

indices_selecionados = st.sidebar.multiselect('Selecione os índices',COLUNAS_ANALISE)

col_analises_exc =[c for c in COLUNAS_ANALISE if not c in indices_selecionados]
colunas_selecionadas = st.sidebar.multiselect('Selecione as colunas', col_analises_exc)

valor_selecionado = st.sidebar.selectbox('Selecione  o valor da análise',COLUNAS_VALOR)

metrica_analise = st.sidebar.selectbox('Selecione uma métrica',list(FUNCOES_AGG.keys()))


#PIVOT TABLE
if len(indices_selecionados)>0 and len(colunas_selecionadas)>0:
    metrica_selecioanda = FUNCOES_AGG[metrica_analise]
    
    vendas_pivotada= pd.pivot_table(df_vendas,
                                    index=indices_selecionados,
                                    columns=colunas_selecionadas,
                                    values=valor_selecionado,
                                    aggfunc=metrica_selecioanda)

    #adicionando a coluna de total
    vendas_pivotada['Total']= vendas_pivotada.sum(axis=1)
    vendas_pivotada.loc['Total']= vendas_pivotada.sum(axis=0).to_list()

    st.dataframe(vendas_pivotada)

else:
    st.dataframe(df_vendas)
