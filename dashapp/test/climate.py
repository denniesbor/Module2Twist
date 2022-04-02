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

df_climate =pd.DataFrame(Climate.objects.all().values())

# products
df_product=pd.DataFrame(Productions.objects.all().values())

# fertilizers
df_fert = pd.DataFrame(FertilizerImports.objects.all().values())

# security and stability
df_secur =pd.DataFrame(SecurityAndStability.objects.all().values())

#government spending on agriculture
df_spending = pd.DataFrame(AgricultureSpending.objects.all().values())


# <---------------------------------------->

# 1. merge the dfs
df_com_pr_com = df_com_pr.merge(df_counties, left_on='county_id', right_on='county_id')\
.merge(df_com, left_on='commodity_id', right_on='commodity_id')

df_com_pr_com.rename(columns={'name_x':'county','name_y':'commodity'},inplace=True)

# extract dates of columns
df_com_pr_com['date'] = pd.to_datetime(df_com_pr_com['date'])

df_com_pr_com['year'], df_com_pr_com['month'] = df_com_pr_com['date'].dt.year, df_com_pr_com['date'].dt.month

# 2. Second Merge

df_pri_prod=df_com_pr_com.merge(df_product,left_on=['commodity_id','county_id','year'], 
                                right_on = ['commodity_id','county_id','year'])

#  convert date into datetime object
df_climate['date']=pd.to_datetime(df_climate['date'])
df_climate['year'], df_climate['month'] = df_climate['date'].dt.year, df_climate['date'].dt.month
df_climate.drop('date', inplace=True,axis=1)

# join the data with the previous datasets on date.
df_pri_prod_cli = df_pri_prod.merge(df_climate, left_on=['year','month'],right_on=['year','month'])

df_ = df_pri_prod_cli.groupby(['date'])[['quantity_per_area','rainfall','temperature']].mean()

fig = px.line(df_.reset_index(), x="date", y=["quantity_per_area","rainfall","temperature"],
              log_y=True)


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('Climate', external_stylesheets=external_stylesheets)
app.layout = html.Div([
    html.Div([
			html.P('Effects of Temperature and Rainfall on yields \
           - log scale'
			)
		], style={'font-size':'16px','text-align': 'center','font-weight':'bold'}),

    dcc.Graph(figure=fig,style={"backgroundColor": "#1a2d46", 'color': '#ffffff'}),
    	html.Div([
			html.P('Change in weathers increases volatility of yields,  \
				and may increase the costs of food as a result of low productivity. \
                There are many climatic factors affecting agricultural productivity. \
                However, for our case the data of interest are the temperature and rainfall as illustrated in the graph above.'
			)
		], style={'margin':20, 'font-size':'16px'}),

])

