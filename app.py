## Dicionários ##
# Dicionário de cores
cores_partidos = {
    'PROS': '#ff9999',
    'SOLIDARIEDADE': '#66b3ff',
    'PSDB': '#99ff99',
    'PODE': '#ffcc99',
    'PSL': '#c2c2f0',
    'PT': '#ff6666',
    'PDT': '#0D47A1',
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
df_init = pd.read_csv('df_16_20_PREF_VER.csv')
shapefile = gpd.read_file('data/Limite_Bairros.shp')

# Preparação dataframe >>>> TEM QUE PADRONIZAR OS CARGOS
df_init.loc[df_init['DS_CARGO'] == 'PREFEITO', 'LEGENDA'] = 0
df_init.rename(columns={'NM_BAIRRO': 'BAIRRO'}, inplace=True)
df_init['BAIRRO'] = df_init['BAIRRO'].map(mapeamento_bairros)

# Organização layout
st.set_page_config(layout="wide")
cargo = st.sidebar.radio("Escolha o cargo", ["PREFEITO", "VEREADOR"], horizontal=True)
year = st.sidebar.selectbox("Ano", df_init["ANO_ELEICAO"].unique())

st.title(f'Dados Eleitorais - {year}')

df = df_init[df_init['ANO_ELEICAO'] == year]
df = df[df['DS_CARGO'] == cargo]

## Grafico 0 ##
if cargo == 'VEREADOR':
    df_top15_ver = df.groupby(['NM_VOTAVEL','SG_PARTIDO','LEGENDA'])['QT_VOTOS'].sum().reset_index()
    df_top15_ver = df_top15_ver[df_top15_ver['LEGENDA'] == 0]
    df_top15_ver = df_top15_ver.sort_values(by='QT_VOTOS', ascending=False).head(15)

    fig0 = px.bar(
    df_top15_ver, 
    x='NM_VOTAVEL', 
    y='QT_VOTOS', 
    title=f'Candidatos a vereador mais votados em {year}',
    color='SG_PARTIDO',
    color_discrete_map=cores_partidos,
    labels={'QT_VOTOS': 'Total de Votos', 'NM_VOTAVEL': 'Candidato'},
    category_orders={"NM_VOTAVEL": df_top15_ver['NM_VOTAVEL']}
     )
    
    st.plotly_chart(fig0)

if cargo == 'PREFEITO':
    df_top4_pref = df[df['NM_VOTAVEL'] != 'VOTO NULO' ]
    df_top4_pref = df_top4_pref[df_top4_pref['NM_VOTAVEL'] != 'VOTO BRANCO' ]

    total_votos = df_top4_pref['QT_VOTOS'].sum()

    df_top4_pref = df_top4_pref.groupby(['NM_VOTAVEL','SG_PARTIDO'])['QT_VOTOS'].sum().reset_index()
    df_top4_pref = df_top4_pref.sort_values(by='QT_VOTOS', ascending=False).head(4)
    df_top4_pref['PERCENTUAL_VOTOS'] = (df_top4_pref['QT_VOTOS'] / total_votos) * 100

    fig0 = px.bar(
    df_top4_pref, 
    x='NM_VOTAVEL', 
    y='PERCENTUAL_VOTOS', 
    title=f'Top 4 Candidatos a prefeito mais votados - {year}',
    color='SG_PARTIDO',
    color_discrete_map=cores_partidos,  
    labels={'PERCENTUAL_VOTOS': 'Porcentagem de Votos (%)', 'QT_VOTOS': 'Votos', 'NM_VOTAVEL': 'Candidato'}
    )

    st.plotly_chart(fig0)

## Gráfico 1 - Paridos x Zona ##

df_grouped_part = df.groupby(['NR_ZONA', 'SG_PARTIDO'])['QT_VOTOS'].sum().reset_index()

st.title('Partidos e Candidatos mais votados por Zona Eleitoral')

# Dropdown para selecionar a zona eleitoral
zonas_unicas = df_grouped_part['NR_ZONA'].unique()
zona_selecionada = st.selectbox('Selecione a Zona Eleitoral', zonas_unicas)

df_filtrado_part = df_grouped_part[df_grouped_part['NR_ZONA'] == zona_selecionada]

df_votos_zona = df.groupby(['NR_ZONA'])['QT_VOTOS'].sum().reset_index()
total_votos_zona = df_votos_zona[df_votos_zona['NR_ZONA'] == zona_selecionada]['QT_VOTOS'].values[0]

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

st.markdown(f"""
<div style="font-size:24px; font-weight:bold;">
    🗳️ Total de votos na zona {zona_selecionada}: <span>{total_votos_zona}</span>
</div>
""", unsafe_allow_html=True)

####
## Gráfico 2 - Paridos x BAirro ##

df_grouped_part_bairro = df.groupby(['BAIRRO', 'SG_PARTIDO'])['QT_VOTOS'].sum().reset_index()

st.title('Partidos e Candidatos mais votados por Bairro')

# Dropdown para selecionar a zona eleitoral
bairros_unicos = df_grouped_part_bairro['BAIRRO'].unique()
bairro_selecionado = st.selectbox('Selecione o Bairro', bairros_unicos)

df_filtrado_part_bairro = df_grouped_part_bairro[df_grouped_part_bairro['BAIRRO'] == bairro_selecionado]

df_votos_bairro = df.groupby(['BAIRRO'])['QT_VOTOS'].sum().reset_index()
total_votos_bairro = df_votos_bairro[df_votos_bairro['BAIRRO'] == bairro_selecionado]['QT_VOTOS'].values[0]
# Ordenar os partidos 
df_top6_part_bairro = df_filtrado_part_bairro.sort_values(by='QT_VOTOS', ascending=False).head(6)

fig3 = px.bar(
    df_top6_part_bairro, 
    x='SG_PARTIDO', 
    y='QT_VOTOS', 
    title=f'Partidos mais votados no bairro {bairro_selecionado}',
    color='SG_PARTIDO',
    color_discrete_map=cores_partidos,
    labels={'QT_VOTOS': 'Total de Votos', 'SG_PARTIDO': 'Partido'},
)

## Gráfico 2 - Candidatos x Zona ##

df_grouped_cand_bairro = df.groupby(['BAIRRO', 'SG_PARTIDO', 'NM_VOTAVEL', 'LEGENDA'])['QT_VOTOS'].sum().reset_index()
df_grouped_cand_bairro = df_grouped_cand_bairro[df_grouped_cand_bairro['LEGENDA'] == 0]

df_filtrado_cand_bairro = df_grouped_cand_bairro[df_grouped_cand_bairro['BAIRRO'] == bairro_selecionado]

df_top6_cand_bairro = df_filtrado_cand_bairro.sort_values(by='QT_VOTOS', ascending=False).head(6)

fig4 = px.bar(
    df_top6_cand_bairro, 
    x='NM_VOTAVEL', 
    y='QT_VOTOS', 
    title=f'Candidatos mais votados no bairro {bairro_selecionado}',
    color='SG_PARTIDO',
    color_discrete_map=cores_partidos,
    labels={'QT_VOTOS': 'Total de Votos', 'NM_VOTAVEL': 'Candidato'},
)

# Exibição
col1, col2 = st.columns([2, 2])

with col1:
    st.plotly_chart(fig3)

with col2:
    st.plotly_chart(fig4)

st.markdown(f"""
<div style="font-size:24px; font-weight:bold;">
    🗳️ Total de votos no bairro {bairro_selecionado}: <span>{total_votos_bairro}</span>
</div>
""", unsafe_allow_html=True)

###
#### top 10 bairros ###

df_top_bairros = df.groupby(['BAIRRO', 'SG_PARTIDO', 'NM_VOTAVEL', 'LEGENDA'])['QT_VOTOS'].sum().reset_index()
df_top_bairros = df_top_bairros[df_top_bairros['LEGENDA'] == 0]

st.title('Bairros com mais voto por candidato')

df_top_bairros['CANDIDATO_PARTIDO'] = df_top_bairros['NM_VOTAVEL'] + ' - ' + df_top_bairros['SG_PARTIDO']

# Dropdown para selecionar o candidato com partido
cand_unicos = df_top_bairros['CANDIDATO_PARTIDO'].unique()
candpart_selecionado = st.selectbox('Selecione o Candidato', cand_unicos)

cand_selecionado, cand_partido = candpart_selecionado.split(' - ')
# Dropdown para selecionar a zona eleitoral
##cand_unicos = df_top_bairros['NM_VOTAVEL'].unique()
#cand_selecionado = st.selectbox('Selecione o Candidato', cand_unicos)

df_filtrado_top_bairros = df_top_bairros[df_top_bairros['NM_VOTAVEL'] == cand_selecionado]

df_top10_bairros = df_filtrado_top_bairros.sort_values(by='QT_VOTOS', ascending=False).head(10)

fig5 = px.bar(
    df_top10_bairros, 
    x='BAIRRO', 
    y='QT_VOTOS', 
    title=f'Bairros com mais votos em {cand_selecionado}',
    color='SG_PARTIDO',
    color_discrete_map=cores_partidos,
    labels={'QT_VOTOS': 'Total de Votos', 'BAIRRO': 'Bairro'},
)

st.plotly_chart(fig5)

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
dados_geoespaciais = shapefile.merge(df_final, on='BAIRRO')
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
    dados_geoespaciais,
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

dados = shapefile.merge(votos_filtrados, on='BAIRRO')

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

if cargo == 'VEREADOR':
## Grafico candidato vereador ##

    st.title('Distribuição de votos em candidatos por bairro')

    df_grouped_bairros_candidato = df.groupby(['BAIRRO', 'NM_VOTAVEL'])['QT_VOTOS'].sum().reset_index()
    df_grouped_bairros_candidato.dropna(subset=['BAIRRO'], inplace=True)
    candidatos = df_grouped_bairros_candidato['NM_VOTAVEL'].unique()
    candidato_selecionado = st.selectbox('Selecione o candidato', candidatos)

    votos_filtrados_candidato = df_grouped_bairros_candidato[df_grouped_bairros_candidato['NM_VOTAVEL'] == candidato_selecionado]
    dados_candidato = shapefile.merge(votos_filtrados_candidato, on='BAIRRO')


    mapa_c = folium.Map(location=[-5.79448, -35.211], zoom_start=12, tiles='cartodb positron')
    choropleth_c = folium.Choropleth(
    geo_data=dados_candidato,
    name='choropleth',
    data=dados_candidato,
    columns=['BAIRRO', 'QT_VOTOS'],
    key_on='feature.properties.BAIRRO',
    fill_color='YlOrRd',
    fill_opacity=0.9,
    line_opacity=0.2,
    legend_name='Quantidade de Votos por Candidato'
    ).add_to(mapa_c)

    tooltip_c = GeoJsonTooltip(
    fields=['BAIRRO', 'QT_VOTOS'],
    aliases=['Bairro:', 'Quantidade de Votos:'],
    localize=True
    )
    choropleth_c.geojson.add_child(tooltip_c) #

    mapa_c.save('mapa_c.html')
    st.components.v1.html(open('mapa_c.html', 'r').read(), height=600)

elif cargo == 'PREFEITO':
    ## Gráfico 3 ##
    st.title('Candidato mais votados por Bairro')

    df_ver = df_init[df_init['ANO_ELEICAO'] == year]
    df_ver = df_ver[df_ver['DS_CARGO'] == 'VEREADOR']
    df_ver = df_ver.groupby(['BAIRRO', 'SG_PARTIDO', 'NM_VOTAVEL', 'LEGENDA'])['QT_VOTOS'].sum().reset_index()
    df_ver = df_ver[df_ver['LEGENDA'] == 0]
    df_ver = df_ver[df_ver['NM_VOTAVEL'] != 'VOTO NULO']
    df_ver = df_ver[df_ver['NM_VOTAVEL'] != 'VOTO BRANCO']

    df_grouped_prefbairros = df.groupby(['BAIRRO', 'SG_PARTIDO', 'NM_VOTAVEL'])['QT_VOTOS'].sum().reset_index()

    # Partido com mais votos em cada bairro
    df_grouped_prefbairros['rank'] = df_grouped_prefbairros.groupby('BAIRRO')['QT_VOTOS'].rank(method='first', ascending=False)
    df_ver['rank'] = df_ver.groupby('BAIRRO')['QT_VOTOS'].rank(method='first', ascending=False)

    # Partido mais votado (rank 1) e o segundo mais votado (rank 2)
    df_max_votos_ver = df_ver[df_ver['rank'] == 1]
    df_second_place_ver = df_ver[df_ver['rank'] == 2]
    df_third_place_ver = df_ver[df_ver['rank'] == 3]

    df_vencedor_pref = df_grouped_prefbairros[df_grouped_prefbairros['rank'] == 1]

    df_final_pref = df_vencedor_pref.merge(df_max_votos_ver[['BAIRRO', 'SG_PARTIDO', 'NM_VOTAVEL', 'QT_VOTOS']], on='BAIRRO', suffixes=('', '_first'))
    df_final_pref = df_final_pref.merge(df_second_place_ver[['BAIRRO', 'SG_PARTIDO', 'NM_VOTAVEL', 'QT_VOTOS']], on='BAIRRO', suffixes=('', '_second'))
    df_final_pref = df_final_pref.merge(df_third_place_ver[['BAIRRO', 'SG_PARTIDO', 'NM_VOTAVEL', 'QT_VOTOS']], on='BAIRRO', suffixes=('', '_third'))
     
    dados_geoespaciais_2 = shapefile.merge(df_final_pref, on='BAIRRO')
    mapa_pref = folium.Map(location=[-5.79448, -35.211], zoom_start=12, tiles='cartodb positron')

    geojson = GeoJson(
    dados_geoespaciais_2,
    style_function=estilo_bairro,
    tooltip=GeoJsonTooltip(
        fields=['BAIRRO', 'NM_VOTAVEL', 'QT_VOTOS', 'SG_PARTIDO','NM_VOTAVEL_first', 'QT_VOTOS_first', 'SG_PARTIDO_first', 'NM_VOTAVEL_second', 'QT_VOTOS_second','SG_PARTIDO_second', 'NM_VOTAVEL_third', 'QT_VOTOS_third', 'SG_PARTIDO_third'],
        aliases=['Bairro:', 'Prefeito vencedor:', 'Votos do Vencedor:', 'Partido:', '1º Lugar Vereador:', 'Votos:', 'Partido:', '2º Lugar Vereador:', 'Votos:', 'Partido:', '3º Lugar Vereador:', 'Votos:', 'Partido:'],
        localize=True
    )
    ).add_to(mapa_pref)

    # Legenda com base nos partidos do dataframe
    partidos_presentes = df_final['SG_PARTIDO'].unique()
    legend_html = '''
    <div style="position: fixed;
            bottom: 50px; left: 50px; width: 200px; height: auto;
            border:2px solid grey; z-index:9999; font-size:14px;
            background-color:white; padding: 10px;">
    &nbsp; <b>Legenda - Candidato Mais Votado</b> <br>
    '''

    for partido in partidos_presentes:
        cor = cores_partidos.get(partido, '#000000')  
        legend_html += f'&nbsp; <i style="background:{cor};width:10px;height:10px;display:inline-block;"></i>&nbsp; {partido} <br>'

        legend_html += '</div>'

    mapa_pref.get_root().html.add_child(folium.Element(legend_html))
    mapa_pref.save('mapa_prefeito_vereadores.html')

    # Exibição
    st.components.v1.html(open('mapa_prefeito_vereadores.html', 'r').read(), height=600)



