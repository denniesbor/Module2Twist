import pandas as pd
import plotly.express as px 
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import joblib

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from django_plotly_dash import DjangoDash
from sklearn.preprocessing import MinMaxScaler,StandardScaler

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
#
df_sec_fert_spend.drop(['id_x','id_y','id'],inplace=True,axis=1)

# model for training

# final dataframe
df_final = df_pri_prod_cli.merge(df_sec_fert_spend,left_on='year',right_on='year')

# import the model

filename = 'finalized_model.sav'

# load the model from disk
model = joblib.load(filename)

# file to prep dataset

def make_train(df):
    
    """the function scales the data
    """
    
    try:
        df.drop(['county','commodity','quantity_per_area','date','capital'],inplace=True,axis=1)
    except:
        print('error')
    pass
    scaler= StandardScaler()
    scaled_data = scaler.fit_transform(df)

    return scaled_data



# making pred of prices between 2015 -> :

df_pred = df_final.query("year>2014")
df_pred_o = df_pred.copy()
df_pred.pop('unit_price')
df_pred.drop(['id_x','id_y','id_x','id_y'],inplace=True,axis=1)
# preprocess the data
df_pred_x = make_train(df_pred)

predictions = model.predict(df_pred_x)
# add preds to the dataframe

df_pred_o = df_pred_o[['county','commodity','year','date']]
df_pred_o['predictions'] =predictions


# prepare the dash_
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = DjangoDash('Model', external_stylesheets=external_stylesheets)

app.layout = html.Div([

    html.Div([
			html.P('Random Forest Regressor Model Performance Evaluation on Different Commodities'
			)
		], style={'font-size':'16px','text-align': 'center','font-weight':'bold'}),

    dcc.Dropdown(id="select_commodity",
                 options=[
                    {"label":"maize","value":'maize'}, 
                    {"label":"sorghum","value":'sorghum'}, 
                    {"label":"millet","value":'millet'}, 
                    {"label":"wheat","value":'wheat'}, 
                    {"label":"sweetpotatoes","value":'sweetpotatoes'}, 
                     ],
                 
                #  multi=False,
                 value='maize',
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
 
    # container = "The year chosen by user was: {}".format(option_slctd)


    df_ = df_final.query("commodity==@option_slctd")
    df_p =df_pred_o.query("commodity==@option_slctd")
    df_ = df_.groupby(['date','commodity'])['unit_price'].mean()
    df_p = df_p.groupby(['date','commodity'])['predictions'].mean()


    fig = px.line(df_.reset_index(), x="date", y="unit_price", color='commodity', title=f'{option_slctd.upper()}')

    fig.add_trace(
        go.Scatter(x=df_p.reset_index()['date'], y=df_p.reset_index()["predictions"],name="Predicted Value")
    )
   
    return fig