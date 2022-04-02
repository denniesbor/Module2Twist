import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from django_plotly_dash import DjangoDash

import pandas as pd
import numpy as np
import plotly.express as px 
import plotly.graph_objects as go

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

df_pri_prod['population_density'] = df_pri_prod['population_density']/100

df = df_pri_prod.groupby(['county','year','commodity'])[['quantity_per_area','unit_price','population_density']].mean()

df = df.reset_index()

# Prepare dash

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('PriceQuantity', external_stylesheets=external_stylesheets)


app.layout = html.Div([
    html.Div([
			html.P('A graph of yields per unit area against the unit prices for each commodity.The color is commodity, and the size of the bubble is average cost '
			)
		], style={'font-size':'16px','text-align': 'center','font-weight':'bold'}),
        
    dcc.Graph(id='graph-with-slider',animate=True, style={"backgroundColor": "#1a2d46", 'color': '#ffffff'}),
    dcc.Slider(
        max = df['year'].max(),
        step=1,
        value=df['year'].min(),
        marks={str(year): str(year) for year in df['year'].unique()},
        id='year-slider',
        updatemode='drag'
    )
])


@app.callback(
    Output('graph-with-slider', 'figure'),
    Input('year-slider', 'value'))

def update_figure(selected_year):
    
    filtered_df = df[df.year == selected_year]

    fig = px.scatter(filtered_df, x="unit_price", y="quantity_per_area",
                     size="population_density", color="commodity", hover_name="county",
                     log_x=True, size_max=55)

    fig.update_layout(transition_duration=500)

    return fig


