from pathlib import Path
import streamlit as st
import pandas as pd
from utilidades import leitura_de_dados
from datetime import datetime

st.set_page_config(page_title='Adicação Registros', layout="wide")
st.markdown("## Adicionar | Remover Registros")
leitura_de_dados()

df_vendas = st.session_state['dados']['df_vendas']
df_filiais = st.session_state['dados']['df_filiais']
df_produtos = st.session_state['dados']['df_produtos']

st.sidebar.markdown('## Adição de Vendas')

#criando uma coluna cidade/estado no df_filiais

df_filiais['Cidade/Estado'] = df_filiais['cidade'] + '/'+df_filiais['estado']

#campos de selecão
cidades_filiais = df_filiais['Cidade/Estado'].unique()

filial_selecionada = st.sidebar.selectbox('Selecione a filial',cidades_filiais)

vendedores = df_filiais.loc[df_filiais['Cidade/Estado']== filial_selecionada,'vendedores'].iloc[0]

vendedores =vendedores.strip('][').replace("'",'').split(',')

vendedor_selecionado = st.sidebar.selectbox('Selecione um vendedor',vendedores)

produtos = df_produtos['nome'].unique()

produto_selecionado = st.sidebar.selectbox('Selecione um produto',produtos)

nome_cliente = st.sidebar.text_input('Insira o nome do cliente')

genero = st.sidebar.selectbox('Insira o gênero',['feminino','masculino','prefiro não informar'])

forma_pagamento = st.sidebar.selectbox('Insira forma de pagamento',['boleto','pix','crédito'])

bt_adicionar_venda = st.sidebar.button("Adicionar")


if bt_adicionar_venda:
    lista_adicionar = [df_vendas['id_venda'].max()+1,
                       filial_selecionada.split('/')[0],
                       vendedor_selecionado,
                       produto_selecionado,
                       nome_cliente,
                       genero,
                       forma_pagamento
                       ]
    hora_adicionar = datetime.now()

    df_vendas.loc[hora_adicionar] = lista_adicionar
    caminho_dataset= st.session_state['caminho_dataset']
    df_vendas.to_csv(caminho_dataset/'vendas.csv',decimal=',',sep=';')



st.sidebar.markdown('## Remoção de registro de vendas')

id_remocao = st.sidebar.number_input('Id venda a ser removido',0,df_vendas['id_venda'].max())


bt_remover_venda = st.sidebar.button('Remover venda')

if bt_remover_venda:
    df_vendas= df_vendas[df_vendas['id_venda'] != id_remocao]
    caminho_dataset = st.session_state['caminho_dataset']
    df_vendas.to_csv(caminho_dataset/'vendas.csv',decimal=',',sep=';')


st.dataframe(df_vendas,height=800)