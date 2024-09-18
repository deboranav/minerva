## Dicionários ##
# Dicionário de cores
cores_partidos = {
    'PROS': '#ff9999',
    'SOLIDARIEDADE': '#66b3ff',
    'PSDB': '#99ff99',
    'PODE': '#ffcc99',
    'PSL': '#c2c2f0',
    'PT': '#ff6666',
    'PDT': '#c4e17f',
    'PP': '#ffb3e6',
    'PTB': '#ffccff',
    'PC do B': '#c4baff',
    'PSB': '#ffc266',
    'MDB': '#ff6666',
    'REPUBLICANOS': '#99ffcc',
    'PRTB': '#ff9966',
    'PMB': '#9966cc',
    'PSOL': '#ff33cc',
    'PL': '#9999ff',
    'PSC': '#66ffb3',
    'PSD': '#ff99e6',
    'Voto em branco': '#999999',
    'Voto nulo': '#666666',
    'CIDADANIA': '#ffcc00',
    'AVANTE': '#cc6699',
    'PV': '#66ff66',
    'NOVO': '#ff3300',
    'PSTU': '#cc0000',
    'UP': '#99cc00',
    'PATRIOTA': '#3366ff',
    'REDE': '#009999',
    'DC': '#003366',
    'SD': '#b3b300',
    'PMDB': '#cc6699',
    'PSDC': '#ff9933'
}

# Dicionário de mapeamento
mapeamento_bairros = {
    'ALECRIM': 'Alecrim',
    'BARRO VERMELHO': 'Barro Vermelho',
    'BOM PASTOR': 'Bom Pastor',
    'CANDELARIA': 'Candelária',
    'CAPIM MACIO': 'Capim Macio',
    'CIDADE ALTA': 'Cidade Alta',
    'CIDADE DA ESPERANCA': 'Cidade da Esperança',
    'CIDADE NOVA': 'Cidade Nova',
    'DIX-SEPT ROSADO': 'Dix-Sept Rosado',
    'FELIPE CAMARAO': 'Felipe Camarão',
    'GUARAPES': 'Guarapes',
    'IGAPO': 'Igapó',
    'LAGOA AZUL': 'Lagoa Azul',
    'LAGOA NOVA': 'Lagoa Nova',
    'LAGOA SECA': 'Lagoa Seca',
    'MAE LUIZA': 'Mãe Luiza',
    'N.S.DA APRESENTAÇÃO': 'N.S. da Apresentaç',
    'NEOPOLIS': 'Neópolis',
    'NORDESTE': 'Nordeste',
    'NOSSA SENHORA DE NAZARE': 'N.S. do Nazaré',
    'NOVA DESCOBERTA': 'Nova Descoberta',
    'PAJUCARA': 'Pajuçara',
    'PETROPOLIS': 'Petrópolis',
    'PITIMBU': 'Pitimbu',
    'PLANALTO': 'Planalto',
    'PONTA NEGRA': 'Ponta Negra',
    'POTENGI': 'Potengi',
    'PRAIA DO MEIO': 'Praia do Meio',
    'QUINTAS': 'Quintas',
    'REDINHA': 'Redinha',
    'RIBEIRA': 'Ribeira',
    'ROCAS': 'Rocas',
    'SANTOS REIS': 'Santos Reis',
    'TIROL': 'Tirol'
}
#### >>> AUTOMATIZAR DICIONARIO

import pandas as pd
import streamlit as st
import plotly.express as px
import geopandas as gpd
import folium
from folium.features import GeoJsonTooltip, GeoJson

# Arquivos
df_init = pd.read_csv('df_16_20_VER.csv')
#shapefile = gpd.read_file('Limite_bairros.shp')
geojson_data = gpd.read_file('limitebairros.json')

# Preparação dataframe >>>> TEM QUE PADRONIZAR OS CARGOS
df_init.rename(columns={'NM_BAIRRO': 'BAIRRO'}, inplace=True)
df_init['BAIRRO'] = df_init['BAIRRO'].map(mapeamento_bairros)

# Organização layout
st.set_page_config(layout="wide")
year = st.sidebar.selectbox("Ano", df_init["ANO_ELEICAO"].unique())

df = df_init[df_init['ANO_ELEICAO'] == year]

## Gráfico 1 - Paridos x Zona ##

df_grouped_part = df.groupby(['NR_ZONA', 'SG_PARTIDO'])['QT_VOTOS'].sum().reset_index()

st.title('Partidos e Candidatos mais votados por Zona Eleitoral')

# Dropdown para selecionar a zona eleitoral
zonas_unicas = df_grouped_part['NR_ZONA'].unique()
zona_selecionada = st.selectbox('Selecione a Zona Eleitoral', zonas_unicas)

df_filtrado_part = df_grouped_part[df_grouped_part['NR_ZONA'] == zona_selecionada]

# Ordenar os partidos 
df_top6_part = df_filtrado_part.sort_values(by='QT_VOTOS', ascending=False).head(6)

fig = px.bar(
    df_top6_part, 
    x='SG_PARTIDO', 
    y='QT_VOTOS', 
    title=f'Partidos mais votados na zona {zona_selecionada}',
    color='SG_PARTIDO',
    color_discrete_map=cores_partidos,
    labels={'QT_VOTOS': 'Total de Votos', 'SG_PARTIDO': 'Partido'},
)

## Gráfico 2 - Candidatos x Zona ##

df_grouped_cand = df.groupby(['NR_ZONA', 'SG_PARTIDO', 'NM_VOTAVEL', 'LEGENDA'])['QT_VOTOS'].sum().reset_index()
df_grouped_cand = df_grouped_cand[df_grouped_cand['LEGENDA'] == 0]

df_filtrado_cand = df_grouped_cand[df_grouped_cand['NR_ZONA'] == zona_selecionada]

df_top6_cand = df_filtrado_cand.sort_values(by='QT_VOTOS', ascending=False).head(6)

fig2 = px.bar(
    df_top6_cand, 
    x='NM_VOTAVEL', 
    y='QT_VOTOS', 
    title=f'Candidatos mais votados na zona {zona_selecionada}',
    color='SG_PARTIDO',
    color_discrete_map=cores_partidos,
    labels={'QT_VOTOS': 'Total de Votos', 'NM_VOTAVEL': 'Candidato'},
)

# Exibição
col1, col2, col3 = st.columns([2, 2, 1])

with col1:
    st.plotly_chart(fig)

with col2:
    st.plotly_chart(fig2)

with col3:
    st.image('zonas.jpg', caption='Mapa das Zonas Eleitorais')

####

### Gráficos de partido em mapa ###
## Gráfico 3 ##
st.title('Partidos mais votados por Bairro')

df_grouped_bairros = df.groupby(['BAIRRO', 'SG_PARTIDO'])['QT_VOTOS'].sum().reset_index()
df_grouped_bairros.dropna(subset=['BAIRRO'], inplace=True)

# Partido com mais votos em cada bairro
df_grouped_bairros['rank'] = df_grouped_bairros.groupby('BAIRRO')['QT_VOTOS'].rank(method='first', ascending=False)

# Partido mais votado (rank 1) e o segundo mais votado (rank 2)
df_max_votos = df_grouped_bairros[df_grouped_bairros['rank'] == 1]
df_second_place = df_grouped_bairros[df_grouped_bairros['rank'] == 2]

df_final = df_max_votos.merge(df_second_place[['BAIRRO', 'SG_PARTIDO', 'QT_VOTOS']], on='BAIRRO', suffixes=('', '_second'))

# Carrega o shapefile 
dados_geoespaciais = geojson_data.merge(df_final, on='BAIRRO')
mapa = folium.Map(location=[-5.79448, -35.211], zoom_start=12, tiles='cartodb positron')

def estilo_bairro(feature):
    partido = feature['properties']['SG_PARTIDO']
    return {
        'fillColor': cores_partidos.get(partido, '#000000'),  
        'color': 'black',
        'weight': 1,
        'fillOpacity': 0.7,
        'lineOpacity': 0.2
    }

# Adicionar a camada de GeoJSON com as cores
geojson = GeoJson(
   # dados_geoespaciais,
    dados_geoespaciais.__geo_interface__,
    style_function=estilo_bairro,
    tooltip=GeoJsonTooltip(
        fields=['BAIRRO', 'SG_PARTIDO', 'QT_VOTOS', 'SG_PARTIDO_second', 'QT_VOTOS_second'],
        aliases=['Bairro:', 'Partido Vencedor:', 'Votos do Vencedor:', 'Segundo Partido:', 'Votos do Segundo:'],
        localize=True
    )
).add_to(mapa)

# Legenda com base nos partidos do dataframe
partidos_presentes = df_final['SG_PARTIDO'].unique()
legend_html = '''
<div style="position: fixed;
            bottom: 50px; left: 50px; width: 200px; height: auto;
            border:2px solid grey; z-index:9999; font-size:14px;
            background-color:white; padding: 10px;">
 &nbsp; <b>Legenda - Partido Mais Votado</b> <br>
'''

for partido in partidos_presentes:
    cor = cores_partidos.get(partido, '#000000')  
    legend_html += f'&nbsp; <i style="background:{cor};width:10px;height:10px;display:inline-block;"></i>&nbsp; {partido} <br>'

legend_html += '</div>'

mapa.get_root().html.add_child(folium.Element(legend_html))
mapa.save('mapa_partidos_vencedores.html')

# Exibição
st.components.v1.html(open('mapa_partidos_vencedores.html', 'r').read(), height=600)

## Grafico 4 ##
st.title('Distribuição de votos por bairro')


partidos = df_grouped_bairros['SG_PARTIDO'].unique()
partido_selecionado = st.selectbox('Selecione o Partido', partidos)

votos_filtrados = df_grouped_bairros[df_grouped_bairros['SG_PARTIDO'] == partido_selecionado]

#dados = shapefile.merge(votos_filtrados, on='BAIRRO')
dados = geojson_data.merge(df_final, on='BAIRRO')

mapa = folium.Map(location=[-5.79448, -35.211], zoom_start=12, tiles='cartodb positron')

choropleth = folium.Choropleth(
    geo_data=dados,
    name='choropleth',
    data=dados,
    columns=['BAIRRO', 'QT_VOTOS'],
    key_on='feature.properties.BAIRRO',
    fill_color='YlOrRd',
    fill_opacity=0.9,
    line_opacity=0.2,
    legend_name='Quantidade de Votos'
).add_to(mapa)

tooltip = GeoJsonTooltip(
    fields=['BAIRRO', 'QT_VOTOS'],
    aliases=['Bairro:', 'Quantidade de Votos:'],
    localize=True
)
choropleth.geojson.add_child(tooltip)

mapa.save('mapa.html')

# Exibição
st.components.v1.html(open('mapa.html', 'r').read(), height=600)
