import pandas as pd
import json
from urllib.request import urlopen
import plotly.express as px 
import plotly.graph_objects as go

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from django_plotly_dash import DjangoDash

# import models
from dashapp.models import County, Commodity,Productions, CommodityPrices, Climate, FertilizerImports, SecurityAndStability, AgricultureSpending

# load pandas dataframe

df_com_pr = pd.DataFrame(CommodityPrices.objects.all().values())
df_counties = pd.DataFrame(County.objects.all().values())
df_com = pd.DataFrame(Commodity.objects.all().values())


# <---------------------------------------->

with open("kenyan-counties.geojson") as jsonified:
    counties = json.load(jsonified)

'''Loading the JSON files'''

counties_0 = counties
name = list(df_counties.name)
id = list(df_counties.county_id)
key_lookup = dict(zip(name,id))

_counties = ['mombasa', 'kwale', 'kilifi', 'tana river', 'lamu', 'taita-taveta', 'garissa', 'wajir', 'mandera', 
            'marsabit', 'isiolo', 'meru', 'tharaka-nithi', 'embu', 'kitui', 'machakos', 'makueni', 
            'nyandarua', 'nyeri', 'kirinyaga', "murang'a", 'kiambu', 'turkana', 'west pokot', 'samburu', 
            'trans nzoia', 'uasin gishu', 'elgeyo-marakwet', 'nandi', 'baringo', 'laikipia', 'nakuru', 
            'narok', 'kajiado', 'kericho', 'bomet', 'kakamega', 'vihiga', 'bungoma', 'busia', 'siaya', 'kisumu', 
            'homa bay', 'migori', 'kisii', 'nyamira', 'nairobi city']

# corrected county names to match the dataframe

json_count = [file.lower() for file in ['Turkana', 'Marsabit', 'Mandera', 'Wajir', 'West Pokot', 'Samburu', 'Isiolo', 'Baringo', 
'elgeyo-marakwet', 'Trans Nzoia', 'Bungoma', 'Garissa', 'Uasin Gishu', 'Kakamega', 'Laikipia', 
'Busia', 'Meru', 'Nandi', 'Siaya', 'Nakuru', 'Vihiga', 'Nyandarua', 'tharaka-nithi',
'Kericho', 'Kisumu', 'Nyeri', 'Tana River', 'Kitui', 'Kirinyaga', 'Embu', 'Homa Bay', 
'Bomet', 'Nyamira', 'Narok', 'Kisii', "Murang'a", 'Migori', 'Kiambu', 'Machakos', 'Kajiado', 'Nairobi City', 'Makueni', 
'Lamu', 'Kilifi', 'taita-taveta', 'Kwale', 'Mombasa']]

# correct the  names
for i in range(47):
    counties_0["features"][i]['properties']['COUNTY']=json_count[i]


# introduce features in the json files
for feature in counties_0['features']:
    feature['id'] = key_lookup[(feature['properties']['COUNTY'])]


# <---------------------------------------------------->

# merge the dfs
df_com_pr_com = df_com_pr.merge(df_counties, left_on='county_id', right_on='county_id')\
.merge(df_com, left_on='commodity_id', right_on='commodity_id')

df_com_pr_com.rename(columns={'name_x':'county','name_y':'commodity'},inplace=True)



# Prepare dash


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('Choropleth', external_stylesheets=external_stylesheets)


app.layout = html.Div([

        html.Div([
			html.P('The unit costs of wheat, maize, sorghum, millet, and sweet potatoes per region. The gray area indicates no data.'
			)
		], style={'font-size':'16px','text-align': 'center','font-weight':'bold'}),

    dcc.Dropdown(id="select_commodity",
                 options=[
                     {"label": "maize", "value": 'maize'},
                     {"label": "millet", "value": "millet"},
                     {"label": "sorghum", "value": "sorghum"},
                     {"label": "wheat", "value": "wheat"},
                     {"label": 'sweetpotatoes', "value": 'sweetpotatoes'},

                     ],
                 multi=False,
                 value='maize',
                 style={'width': "60%"}
                 ),

    # html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='commodity_prices', animate=True, style={"backgroundColor": "#1a2d46", 'color': '#ffffff'})

])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
  
     Output(component_id='commodity_prices', component_property='figure'),
    [Input(component_id='select_commodity', component_property='value')]
)
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    # container = "The year chosen by user was: {}".format(option_slctd)

    df_ = df_com_pr_com.copy()
    print(df_.head)
    df_ = df_.query('commodity==@option_slctd')
    df_ = df_.groupby(['county','commodity','county_id'])[['unit_price','population_density']].mean()

    df_ = df_.reset_index()
    print(df_.head())
    df_['scaled'] = df_['unit_price']/6


    fig = px.choropleth(df_, geojson=counties_0, 
                        locations='county_id', 
                        color='scaled',
                        color_continuous_scale=px.colors.sequential.YlOrRd,
                        hover_name = 'county',
                        hover_data = ['unit_price','population_density','commodity'],
                        template='plotly_dark'
                            
                            )
                            
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
                    geo = dict(landcolor = 'lightgray',
                    showland = True,
                    showcountries = True,
                    countrycolor = 'gray',
                    countrywidth = 0.5)
                    )
    fig.update_geos(fitbounds='locations', visible=True)
    
    return fig