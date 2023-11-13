from pathlib import Path
import streamlit as st
import pandas as pd
from utilidades import leitura_de_dados
from utilidades import leitura_de_dados,COMISSAO
from datetime import date,timedelta
import plotly.express as px

st.set_page_config(page_title='Visão Geral', layout="wide")

leitura_de_dados()



df_vendas = st.session_state['dados']['df_vendas']
df_filiais= st.session_state['dados']['df_filiais']
df_produtos =st.session_state['dados']['df_produtos']

#------------------------------ mesmo código da page 02
df_produtos = df_produtos.rename(columns={'nome':'produto'})
df_vendas = df_vendas.reset_index()
df_vendas = pd.merge(left= df_vendas,
                     right= df_produtos[['produto','preco']],
                     on='produto',
                     how='left')

df_vendas['comissao']= df_vendas['preco']* COMISSAO
#------------------------------------------------------

df_vendas['data'] = pd.to_datetime(df_vendas['data']).dt.date

data_inicial= st.sidebar.date_input('Data Inicial',df_vendas['data'].min())

data_final= st.sidebar.date_input('Data Final',df_vendas['data'].max())

st.markdown("## Dashboard- Análise de Vendas")

#dataframe filtrado com data inicial e data final
df_vendas_corte = df_vendas[(df_vendas['data']>=data_inicial) & (df_vendas['data']<= data_final)]





col1,col2,col3,col4 = st.columns(4)

#adicionando as metrics
#metric_1 - valor total vendas
valor_total_vendas = f"R$ {df_vendas_corte['preco'].sum():_.2f}"

#fazendo a formatação de moeda R$
valor_total_vendas=valor_total_vendas.replace('.',',').replace('_','.')
col1.metric(' R$ Valor Total Vendas',valor_total_vendas)

#metric_2 - qtd vendas

qtd_vendas = f"{df_vendas_corte['produto'].count():,}"
qtd_vendas= qtd_vendas.replace(',','.')
col2.metric("Total Registro Vendas", qtd_vendas)

#metric_3 - filial maoior faturamento

top1_filial = df_vendas_corte['filial'].value_counts().index[0]
col3.metric(' Filial Com Maior Registro de Vendas',top1_filial)

#metric_4 - vendedor maoior faturamento

top1_vendedor = df_vendas_corte['vendedor'].value_counts().index[0]
col4.metric('Vendedor Com Maior Registro de Vendas',top1_vendedor)

st.divider()

#GRÁFICOS

df_vendas_corte['data'] = pd.to_datetime(df_vendas_corte['data'])
df_vendas_corte['mês'] =df_vendas_corte['data'].dt.month
df_vendas_corte['Nome Mês'] = df_vendas_corte['data'].dt.strftime('%B')
df_vendas_mes =df_vendas_corte.groupby('mês')['preco'].sum().reset_index()
df_vendas_mes.rename(columns={'preco':'faturamento'},inplace= True)


col21,col22,col23= st.columns(3)

fig = px.line(df_vendas_mes,x='mês',y='faturamento',markers=True,title='R$ Faturamento Mensal')
col21.plotly_chart(fig)


#grafico de barra invertida filial

df_vendas_filial = df_vendas_corte.groupby('filial')['preco'].sum().reset_index()
df_vendas_filial.rename(columns={'preco':'faturamento'}, inplace=True)
df_vendas_filial = df_vendas_filial.sort_values(by='faturamento',ascending=True)
fig= px.bar(df_vendas_filial,x='faturamento',y='filial',orientation='h',title="R$ Faturamento por Filial")
col22.plotly_chart(fig)


## grafico de pizza por forma de pagamento

df_vendas_forma_pgto = df_vendas_corte.groupby('forma_pagamento')['preco'].sum().reset_index()
df_vendas_forma_pgto.rename(columns={'preco':'faturamento'},inplace=True)

fig = px.pie(df_vendas_forma_pgto,names='forma_pagamento',values='faturamento',title='Forma de Pagamento')
col23.plotly_chart(fig)


col24,col25,col26 = st.columns(3)

#grafico de barra invertida vendedor

df_vendas_vendedor = df_vendas_corte.groupby('vendedor')['preco'].sum().reset_index()
df_vendas_vendedor.rename(columns={'preco':'faturamento'}, inplace=True)
df_vendas_vendedor= df_vendas_vendedor.sort_values(by='faturamento',ascending=True)
fig= px.bar(df_vendas_vendedor,x='faturamento',y='vendedor',orientation='h',title="R$ Faturamento por Vendedor")
col24.plotly_chart(fig)

#grafico de barra  vendedor

df_vendas_produto = df_vendas_corte.groupby('produto')['preco'].sum().reset_index()
df_vendas_produto.rename(columns={'preco':'faturamento'}, inplace=True)
df_vendas_produto= df_vendas_produto.sort_values(by='faturamento',ascending=True)
fig= px.bar(df_vendas_produto,x='faturamento',y='produto',orientation='h',title="R$ Faturamento por Produto")
col25.plotly_chart(fig)


#grafico barra genero

df_vendas_genero = df_vendas_corte.groupby('cliente_genero')['preco'].sum().reset_index()
df_vendas_genero.rename(columns={'preco':'faturamento'}, inplace=True)
df_vendas_genero= df_vendas_genero.sort_values(by='faturamento',ascending=True)
fig= px.pie(df_vendas_genero,names='cliente_genero',values='faturamento',hole=0.4,title="Faturamento por Gênero")
col26.plotly_chart(fig)
