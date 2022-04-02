import pandas as pd
import plotly.express as px 

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


# merge the dfs
df_com_pr_com = df_com_pr.merge(df_counties, left_on='county_id', right_on='county_id')\
.merge(df_com, left_on='commodity_id', right_on='commodity_id')

df_com_pr_com.rename(columns={'name_x':'county','name_y':'commodity'},inplace=True)



# Prepare dash


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


app = DjangoDash('PriceDistCounty', external_stylesheets=external_stylesheets)


app.layout = html.Div([

    html.Div([
			html.P('An interactive graph showing agricultural commodities unit-price distribution across the country'
			)
		], style={'font-size':'16px','text-align': 'center','font-weight':'bold'}),

    dcc.Dropdown(id="select_commodity",
                 options=[
                    {"label":"mombasa","value":'mombasa'}, 
                    {"label":"kwale","value":'kwale'}, 
                    {"label":"kilifi","value":'kilifi'}, 
                    {"label":"tana river","value":'tana river'}, 
                    {"label":"lamu","value":'lamu'}, 
                    {"label":"taita-taveta}","value":'taita-taveta'}, 
                    {"label":"garissa","value":'garissa'}, 
                    {"label":"wajir","value":'wajir'}, 
                    {"label":"mandera","value":'mandera'}, 
                    {"label":"marsabit","value":'marsabit'}, 
                    {"label":"isiolo","value":'isiolo'}, 
                    {"label":"meru","value":'meru'}, 
                    {"label":"tharaka-nithi","value":'tharaka-nithi'}, 
                    {"label":"embu","value":'embu'}, 
                    {"label":"kitui","value":'kitui'}, 
                    {"label":"machakos","value":'machakos'}, 
                    {"label":"makueni","value":'makueni'}, 
                    {"label":"nyandarua","value":'nyandarua'}, 
                    {"label":"nyeri","value":'nyeri'}, 
                    {"label":"kirinyaga","value":'kirinyaga'},
                    {"label":"murang'a","value":"murang'a"}, 
                    {"label":"kiambu","value":'kiambu'}, 
                    {"label":"turkana","value":'turkana'}, 
                    {"label":"west pokot","value":'west pokot'}, 
                    {"label":"samburu","value":'samburu'}, 
                    {"label":"trans nzoia","value":'trans nzoia'}, 
                    {"label":"uasin gishu","value":'uasin gishu'}, 
                    {"label":"elgeyo-marakwet","value":'elgeyo-marakwet'}, 
                    {"label":"nandi","value":'nandi'}, 
                    {"label":"baringo","value":'baringo'}, 
                    {"label":"laikipia","value":'laikipia'}, 
                    {"label":"nakuru","value":'nakuru'}, 
                    {"label":"narok","value":'narok'}, 
                    {"label":"kajiado","value":'kajiado'}, 
                    {"label":"kericho","value":'kericho'}, 
                    {"label":"bomet","value":'bomet'}, 
                    {"label":"kakamega","value":'kakamega'}, 
                    {"label":"vihiga","value":'vihiga'}, 
                    {"label":"bungoma","value":'bungoma'}, 
                    {"label":"busia","value":'busia'}, 
                    {"label":"siaya","value":'siaya'},
                    {"label":"kisumu","value":'kisumu'}, 
                    {"label":"homa bay","value":'homa bay'}, 
                    {"label":"migori","value":'migori'}, 
                    {"label":"kisii","value":'kisii'}, 
                    {"label":"nairobi city","value":'nairobi city'},
                    {"label":"nyamira","value":'nyamira'}, 

                     ],
                 
                #  multi=False,
                 value='nairobi city',
                 style={'width': "40%"}
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
    df_ = df_.query('county==@option_slctd')
    df_ = df_.groupby(['date','commodity'])['unit_price'].mean()

    df_ = df_.reset_index()
    
    fig = px.line(df_,
            x="date", y="unit_price", color='commodity', 
            title=f'{option_slctd.upper()} COUNTY')
   
    return fig