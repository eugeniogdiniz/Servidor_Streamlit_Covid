from pandas.io.clipboards import read_clipboard
import streamlit as st
import pandas as pd
import json
import plotly as plt
import plotly.express as px

df = pd.read_csv('covid.csv')
df['date']  = pd.to_datetime(df['date'])
df.info()

primeiro_dia = df['date'].min()
ultimo_dia = df['date'].max()
dias_percorridos = str(ultimo_dia - primeiro_dia)

st.title("Análise da evolução da Covid-19 no Mundo")
st.sidebar.markdown('Feito por : Eugênio G. Diniz')

st.markdown('----')
st.markdown('#Sobre a Base de Dados')
st.markdown(f'''Os primeiros casos do coronavírus (Covid-19) tiveram origem no mercado de frutos do mar da cidade de Wuhan localizada na China, 
as primeiras ocorrências foram relatadas na virada do ano 31/12/2020 e a incidência aumentou de maneira exponencial nas primeiras semanas..

A base de dados tem como primeiro registro o dia {primeiro_dia},
enquanto que seu ultimo registro está computado em {ultimo_dia}, tendo um período total de {dias_percorridos[0:4]} dias.

Abaixo é possivel observar os países do mundo com o total de casos registrados nesse período.
''')

total_case = df.groupby('Country')['total_cases'].mean()
st.write("Média de Casos de Covind no Mundo")
st.bar_chart(total_case)

st.markdown(f'''Por meio do filtro lateral é possivel observar os dados aqui registrados por páis.
''')

#Análise por páis
df_country = df['Country'].drop_duplicates()

#Filtro por páis
filtro_pais = st.sidebar.selectbox(
    'Escolha o País:',
    df_country
)

#Data Frame
df_pais = df[df['Country'] == filtro_pais]
st.write(f"Covid 19 - Amostra do país: {filtro_pais}")
st.dataframe(df_pais)

df_new_cases = df['new_cases']


st.write("Evolução dos Casos")

df_media_new_case = int(df_new_cases.mean())
df_soma_total_case = int((df['total_cases'].sum())/1000000)

st.markdown(f'''No gráfico abaixo é possivel ver a evolução dos novos casos de covid ao longo do período registrado.

A média de novos casos ao longo do período foi de {df_media_new_case}, sendo carregada no segundo trimeste do ano de 2020.

A soma de casos no período equivalem à {df_soma_total_case} milhões de casos em todo o mundo.

''')

fig = px.bar(x = df['date'],
            y = df_new_cases,
            orientation = 'v', title = "Evolução dos novos casos de Covid no mundo",
            labels = {'x':'Período', 'y':'Novos Casos'},
            width = 800, height = 600)

st.plotly_chart(fig)

df_pais_media_total = df_pais['total_cases'].sum()
df_pais_media_dia = int(df_pais['new_cases'].mean())
df_pais_total_testes = int(df_pais['total_tests'].sum())
df_pais_media_testes = int(df_pais['new_tests'].mean())



st.markdown(f'''Buscando facilitar a leitura e a análise, por meio do filtro lateral é possivel observar que o(a)
{filtro_pais} teve um total de {df_pais_media_total} casos de Covid ao longo do período análisado com uma média diária de
{df_pais_media_dia} novos casos.

Buscando medidas de prevensão contra a Covid, foram feitos um total de {df_pais_total_testes} com uma testagem diária média de
{df_pais_media_testes}.

''')

fig = px.bar(x = df_pais['date'],
            y = [df_pais['new_cases'], df_pais['new_tests']],
            orientation = 'v', title = "Evolução dos novos casos de Covid no mundo",
            labels = {'x':'Período', 'y':'Novos Casos'},
            width = 800, height = 600)

st.plotly_chart(fig)