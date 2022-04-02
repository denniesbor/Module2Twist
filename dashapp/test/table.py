import pandas as pd
import plotly.express as px 
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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

df_secur.rename(columns={'index':'security_index'})
df_fert.rename(columns={'quantity':'fertilizer_imported'},inplace=True)

df_sec_fert_spend = df_secur.merge(df_fert, how='outer',left_on='year',right_on='year')\
    .merge(df_spending,how='outer',left_on='year',right_on='year')

df_sec_fert_spend = df_sec_fert_spend.query("year > 2010")
df_sec_fert_spend.fillna(0,inplace=True)
df_sec_fert_spend.reset_index(inplace=True,drop=True)
# Prepare dash

df_sec_fert_spend.drop(['id_x','id_y','id'],inplace=True,axis=1)

fig = make_subplots(
    rows=3, cols=2,
    shared_xaxes=True,
    vertical_spacing=0.03,
    specs=[[{"type": "table","colspan": 2},None],
            [{"type": "scatter"},{"type": "scatter"}],
            [{"type": "scatter"},{"type": "scatter"}]]

)

fig.add_trace(
    go.Scatter(
        x=df_sec_fert_spend["year"],
        y=df_sec_fert_spend["index"],
        mode="lines",
        name="Security Index",
    ),
    row=2, col=1
)
fig.add_trace(
    go.Scatter(
        x=df_sec_fert_spend["year"],
        y=df_sec_fert_spend["totalexpenditure"],
        mode="lines",
        name="Total Government Expenditure"
    ),
    row=2, col=2
)

fig.add_trace(
    go.Scatter(
        x=df_sec_fert_spend["year"],
        y=df_sec_fert_spend["fertilizer_imported"],
        mode="lines",
        name="Fertilizer imported in MT"
    ),
    row=3, col=1
)

fig.add_trace(
    go.Scatter(
        x=df_sec_fert_spend["year"],
        y=df_sec_fert_spend["agriculturespending"],
        mode="lines",
        name="Govt Spending on Agric"
    ),
    row=3, col=2
)

fig.add_trace(
    go.Table(
        header=dict(
            values=["Year", "Security<br>index", "Fertilizer<br>Imported",
                    "Total<br>Expenditure", "Agriculture<br>Spending"],
            font=dict(size=10),
            align="left"
        ),
        cells=dict(
            values=[df_sec_fert_spend[k].tolist() for k in df_sec_fert_spend.columns[0:]],
            align = "left")
    ),
    row=1, col=1
)
fig.update_layout(
    height=800,
    showlegend=False,
)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('Table', external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([
        html.P('A table and plots of government expenditure on agriculture, fertilizer imported in metric tons and stability index'
        )
    ], style={'font-size':'16px','text-align': 'center','font-weight':'bold'}),

    dcc.Graph(figure=fig)
])