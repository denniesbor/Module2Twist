from django.shortcuts import render

import pandas as pd
from dashapp.models import County,CommodityPrices,Commodity



import plotly.express as px
import plotly.graph_objs as go
from plotly.offline import plot

# Pandas Dataframes

df_com_pr = pd.DataFrame(County.objects.all().values())
df_counties = pd.DataFrame(CommodityPrices.objects.all().values())
df_com = pd.DataFrame(Commodity.objects.all().values())

df_com_pr_com = df_com_pr.merge(df_counties, left_on='county_id', right_on='county_id')\
.merge(df_com, left_on='commodity_id', right_on='commodity_id')

df_com_pr_com.rename(columns={'name_x':'county','name_y':'commodity'},inplace=True)

# external sheets

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


def index(request):

    return render(request, 'welcome.html')

def charts(request):
    # Pandas DataFrame Query
    
    def pop_dist():
        
        df_ = df_com_pr_com.groupby(['county','commodity'])['unit_price'].mean()

        fig = px.pie(df_.reset_index(), values='unit_price', names='county', \
             title='Average prices of the commodities in the counties',labels=False)
        
        fig.update_layout(height=400)
        plot_div = plot(fig,output_type='div',include_plotlyjs=False)
        
        return plot_div
    
    context = {
        "plot":pop_dist()
    }
    return render(request, 'charts.html', context=context)
