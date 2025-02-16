import streamlit as st
import matplotlib.pyplot as plt
from extracao import get_bcb_data
import pandas as pd
import plotly.express as px

# Configuração do layout do Streamlit
st.set_page_config(layout="wide", page_title="Painel Econômico")

# Título do painel
st.title("Painel Econômico - Indicadores do Brasil")

# Sidebar para filtros de data
st.sidebar.header("Filtros")
start_date = st.sidebar.date_input("Data Inicial", value=pd.Timestamp("2000-01-01"))
end_date = st.sidebar.date_input("Data Final", value=pd.Timestamp("2025-01-01"))

# Converter os filtros de data para o formato datetime64[ns]
start_date = pd.Timestamp(start_date)
end_date = pd.Timestamp(end_date)

lista_indicadores = {
    "Inflação (12 meses)": 13522,
    "Dívida bruta do governo geral (% PIB)": 13762,
    "Meta para a inflação": 13521,
    "Taxa Selic": 432,
    "Taxa de Desemprego": 24369
}

df = {}

for indicador, id in lista_indicadores.items():
    data = get_bcb_data(id)
    if data is not None and not data.empty:
        data["data"] = pd.to_datetime(data["data"])  # Garantir que a coluna "data" seja datetime
        df[indicador] = data[(data["data"] >= start_date) & (data["data"] <= end_date)]

st.subheader("Indicadores Econômicos")

col1, col2 = st.columns(2)  

# Gráfico 1: Inflação
with col1:
    if "Inflação (12 meses)" in df and not df["Inflação (12 meses)"].empty:
        fig1 = px.line(df["Inflação (12 meses)"], x="data", y="valor", title="Inflação (12 meses)", 
                       labels={"valor": "Inflação (%)", "data": "Ano"})
        st.plotly_chart(fig1, use_container_width=True)

# Gráfico 2: Dívida Bruta do Governo
with col2:
    if "Dívida bruta do governo geral (% PIB)" in df and not df["Dívida bruta do governo geral (% PIB)"].empty:
        fig2 = px.line(df["Dívida bruta do governo geral (% PIB)"], x="data", y="valor", 
                       title="Dívida bruta do governo geral (% PIB)", labels={"valor": "% PIB", "data": "Ano"})
        st.plotly_chart(fig2, use_container_width=True)

# Gráfico 3: Taxa Selic
with col1:
    if "Taxa Selic" in df and not df["Taxa Selic"].empty:
        fig3 = px.line(df["Taxa Selic"], x="data", y="valor", title="Taxa Selic", 
                       labels={"valor": "Selic (%)", "data": "Ano"})
        st.plotly_chart(fig3, use_container_width=True)

# Gráfico 4: Taxa de Desemprego
with col2:
    if "Taxa de Desemprego" in df and not df["Taxa de Desemprego"].empty:
        fig4 = px.line(df["Taxa de Desemprego"], x="data", y="valor", title="Taxa de Desemprego", 
                       labels={"valor": "Taxa de Desemprego (%)", "data": "Ano"})
        st.plotly_chart(fig4, use_container_width=True)
