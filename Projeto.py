import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots


 

dataset = st.beta_container()

st.sidebar.title('Relatórios de Venda')

vendasPorAno = st.sidebar.button('Total de Vendas por Ano')
vendasPorCategoria = st.sidebar.button('Total de Vendas por Categoria')
vendasPorCategoriaAno = st.sidebar.button('Total de Vendas por Categoria por Ano')
vendasPorAnoCategoria = st.sidebar.button('Total de Vendas por Ano e Categoria')
VendasCategoriaMesesAno = st.sidebar.button('Total de Vendas por Categoria pelos Meses para cada Ano')
ProdutoMaisVendidoFabricante = st.sidebar.button('Produtos mais Vendido por cada Fabricante')
VendasLojasCategoria = st.sidebar.button('Vendas das Lojas por Categoria')
RankingProdutosMaioresVendasGeralLoja = st.sidebar.button('Ranking dos Produtos com maiores Vendas no geral e por Loja')
RankingProdutosMenoresVendasGeralLoja = st.sidebar.button('Ranking dos Produtos com menores Vendas no geral e por Loja')
RankingProdutosMaisRentaveisGeralLoja = st.sidebar.button('Ranking dos Produtos mais rentáveis no geral e por Loja')
RankingVendasLoja = st.sidebar.button('Ranking vendas por Lojas')
RankingVendedoresMaiorValorVendasLojaAno = st.sidebar.button('Ranking dos vendedores com maior valor de venda por Loja e por Ano')

with dataset:
    st.title('Ciência de Dados')
    st.header("Análise de Vendas")
    df = pd.read_csv('Vendas.csv',sep=';',encoding='latin-1',decimal=",")    

if vendasPorAno:
    df['Data Venda'] = pd.to_datetime(df['Data Venda'])
    df['Ano'] = df['Data Venda']. dt.to_period('Y').astype(str)
    vendas_ano = df.groupby('Ano')['ValorVenda'].sum().reset_index()
    fig = px.bar(
            vendas_ano, 
            x = "Ano",
            y = "ValorVenda",
            title = "TOTAL DE VENDAS POR ANO ",
            width = 900,
            height = 700,
            color="Ano",
            color_discrete_sequence = px.colors.qualitative.Set1
    )  
    st.plotly_chart(fig)

elif  vendasPorCategoria:
    vendas_categoria = df.groupby(["Categoria"])["ValorVenda"].sum() 
    fig = px.bar(
            vendas_categoria,
            y= "ValorVenda",           
            title = "TOTAL DE VENDAS POR CATEGORIA",
            width = 900,
            height = 700,
            color = "ValorVenda",
            color_discrete_sequence = px.colors.qualitative.Set1
    )  
    st.plotly_chart(fig)

elif vendasPorCategoriaAno:
    df['Data Venda'] = pd.to_datetime(df['Data Venda'])
    df['Ano'] = df['Data Venda']. dt.to_period('Y').astype(str)
    vendas_categoria_ano = pd.pivot_table(df,index=['Categoria'],values= 'ValorVenda',columns=['Ano'], aggfunc = 'sum')
    fig = px.bar(
            vendas_categoria_ano,
            title = "TOTAL DE VENDAS POR CATEGORIA POR ANO",
            width = 900,
            height = 700,
            barmode='group'
    )  
    st.plotly_chart(fig) 

elif vendasPorAnoCategoria:
    df['Data Venda'] = pd.to_datetime(df['Data Venda'])
    df['Ano'] = df['Data Venda']. dt.to_period('Y').astype(str)
    vendas_por_ano_categoria = pd.pivot_table(df,index=['Ano'],values= 'ValorVenda',columns=['Categoria'], aggfunc = 'sum')
    fig = px.bar(
            vendas_por_ano_categoria,
            title = "TOTAL DE VENDAS POR ANO E CATEGORIA",
            width = 900,
            height = 700,
            barmode='group'
    )  
    st.plotly_chart(fig)

elif VendasCategoriaMesesAno:
    df['Data Venda'] = pd.to_datetime(df['Data Venda'])
    df['Mes_Ano'] = df['Data Venda'].dt.to_period('M').astype(str)
    vendas_categoria_mes_ano = pd.pivot_table(df,index=['Categoria'],columns=['Mes_Ano'],values="ValorVenda", aggfunc = 'sum')
    fig = px.bar(
        vendas_categoria_mes_ano, 
        title ="TOTAL DE VENDAS POR CATEGORIA PELOS MESES PARA CADA ANO",
        width = 1200,
        height = 700,
        color_discrete_sequence = px.colors.qualitative.Vivid,
        barmode='group'
    ) 
    st.plotly_chart(fig)

elif ProdutoMaisVendidoFabricante:
    produto_mais_vendido_fabricante = pd.pivot_table(df,index=['Produto'],columns=['Fabricante'],values="ValorVenda", aggfunc = 'sum')
    fig = px.bar(
        produto_mais_vendido_fabricante , 
        title ="PRODUTOS MAIS VENDIDO POR CADA FABRICANTE ",
        width = 900,
        height = 700,
        color_discrete_sequence = px.colors.qualitative.D3,
        barmode = 'group'
    ) 
    st.plotly_chart(fig)

elif VendasLojasCategoria:  
    vendas_loja_categoria = pd.pivot_table(df,index=['Loja'],values= 'ValorVenda',columns=['Categoria'], aggfunc = 'sum') 
    fig = px.bar(
        vendas_loja_categoria, 
        title ="VENDAS DAS LOJAS POR CATEGORIA",
        width = 900,
        height = 700,
        color_discrete_sequence = px.colors.qualitative.D3,
        barmode = 'group'
    ) 
    st.plotly_chart(fig)    
    
elif RankingProdutosMaioresVendasGeralLoja:
    ranking_produtos_maiores_venda = df.groupby('Produto').aggregate(np.sum).reset_index().sort_values('ValorVenda',ascending = False)
    fig = px.bar(
            ranking_produtos_maiores_venda,
            x= "Produto",
            y= "ValorVenda",           
            title ="RANKING DOS PRODUTOS COM MAIORES VENDAS NO GERAL ",
            width = 900,
            height = 700,
            color = "Produto",
            color_discrete_sequence = px.colors.qualitative.D3
    )  
    st.plotly_chart(fig)
    st.write(ranking_produtos_maiores_venda)

    ranking_produtos_maiores_venda = df.groupby(['Produto','Loja']).aggregate(np.sum).reset_index().sort_values('ValorVenda',ascending = False)
    fig = px.bar(
            ranking_produtos_maiores_venda,
            x= "Produto",
            y= "ValorVenda",           
            title ="RANKING DOS PRODUTOS COM MAIORES VENDAS POR LOJA",
            width = 900,
            height = 700,
            color = "Loja"
           
    )  
    st.plotly_chart(fig)
    st.write(ranking_produtos_maiores_venda)

elif RankingProdutosMenoresVendasGeralLoja:
    ranking_produtos_menores_venda = df.groupby('Produto').aggregate(np.sum).reset_index().sort_values('ValorVenda',ascending = True)
    fig = px.bar(
            ranking_produtos_menores_venda,
            x= "Produto",
            y= "ValorVenda",           
            title ="RANKING DOS PRODUTOS COM MENORES VENDAS NO GERAL",
            width = 900,
            height = 700,
            color = "Produto",
            color_discrete_sequence = px.colors.qualitative.D3
    )  
    st.plotly_chart(fig)
    st.write(ranking_produtos_menores_venda)

    ranking_produtos_menores_venda = df.groupby(['Produto','Loja']).aggregate(np.sum).reset_index().sort_values('ValorVenda',ascending = True)
    fig = px.bar(
            ranking_produtos_menores_venda,
            x= "Produto",
            y= "ValorVenda",           
            title ="RANKING DOS PRODUTOS COM MENORES VENDAS POR LOJA",
            width = 900,
            height = 700,
            color = "Loja"
    )  
    st.plotly_chart(fig)
    st.write(ranking_produtos_menores_venda)

elif RankingProdutosMaisRentaveisGeralLoja: 
    df["Rentável"]= df['ValorVenda'] - df["preço Custo"] 
    raking_pro_rentavel = df.groupby('Produto').aggregate(np.sum).reset_index().sort_values('Rentável',ascending = False)
    fig = px.bar(
            raking_pro_rentavel,
            x= "Produto",
            y= "Rentável",           
            title ="RANKING DOS PRODUTOS MAIS RENTÁVEIS NO GERAL",
            width = 900,
            height = 700,
            color = "Rentável",
            color_discrete_sequence = px.colors.qualitative.D3
    )  
    st.plotly_chart(fig)
    st.write(raking_pro_rentavel)
    raking_pro_rentavel = df.groupby(['Produto','Loja']).aggregate(np.sum).reset_index().sort_values('Rentável',ascending = False)
    fig = px.bar(
            raking_pro_rentavel,
            x= "Produto",
            y= "Rentável",           
            title ="RANKING DOS PRODUTOS MAIS RENTÁVEIS POR LOJA",
            width = 900,
            height = 700,
            color = "Loja",
            color_discrete_sequence = px.colors.qualitative.D3
    )  
    st.plotly_chart(fig)
    st.write(raking_pro_rentavel)

elif RankingVendasLoja:
    ranking_venda_loja = df.groupby('Loja')['ValorVenda'].sum()
    fig = px.bar(
        ranking_venda_loja.sort_values(ascending=False), 
        y= "ValorVenda",           
        title ="RANKING DE VENDAS POR LOJAS",
        width = 900,
        height = 700,  
        color = "ValorVenda",
        color_discrete_sequence = px.colors.qualitative.Safe
    ) 
       
    st.plotly_chart(fig)
    ranking_venda_loja

elif RankingVendedoresMaiorValorVendasLojaAno:
    df['Data Venda'] = pd.to_datetime(df['Data Venda'])
    df['Ano'] = df['Data Venda']. dt.to_period('Y').astype(str) 
    ranking_vendedores_vendas_loja_ano = pd.DataFrame(df.groupby(['Vendedor','Loja' ,'Ano'],as_index=False).ValorVenda.sum())
    df = ranking_vendedores_vendas_loja_ano.loc[:,['Loja','Ano','Vendedor', 'ValorVenda']]
    df = df.sort_values(by=['Ano','ValorVenda'], ascending=False) 
    fig = px.bar(
            ranking_vendedores_vendas_loja_ano, 
            x ="Vendedor",
            y = "ValorVenda",
            title = "RANKING DE VENDEDORES COM MAIOR VALOR DE VENDAS POR ANO",
            width = 900,
            height = 700,
            color="Ano",
            color_discrete_sequence = px.colors.qualitative.Set1
    )  
    st.plotly_chart(fig)
    ranking_vendedores_vendas_loja_ano[["Vendedor","Loja","ValorVenda","Ano"]]
   
    ranking_vendedores_vendas_loja_ano = pd.DataFrame(df.groupby(['Vendedor', 'Loja'],as_index=False).ValorVenda.sum())
    df = ranking_vendedores_vendas_loja_ano.loc[:,['Loja','Vendedor', 'ValorVenda']]
    df = df.sort_values(by=['Loja','ValorVenda'], ascending=False) 
    fig = px.bar(
            ranking_vendedores_vendas_loja_ano, 
            x ="Vendedor",
            y = "ValorVenda",
            title = "RANKING DE VENDEDORES COM MAIOR VALOR DE VENDAS POR LOJA",
            width = 900,
            height = 700,
            color="Loja",
            color_discrete_sequence = px.colors.qualitative.Set1
    )  
    st.plotly_chart(fig) 
    



   
   
