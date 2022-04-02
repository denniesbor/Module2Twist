app.layout = html.Div([

    html.H1(f"Prices Distribution in the Country", style={'text-align': 'center'}),

    dcc.Dropdown(id="select_commodity",
                 options=[
                     {"label": "maize", "value": 'maize'},
                     {"label": "wheat", "value": "wheat"},
                     {"label": "sweetpotatoes", "value": "sweetpotatoes"},
                     {"label": "sorghum", "value": "sorghum"},
                     {"label": "millet", "value": "millet"},
                     
                     ],
                 multi=False,
                 value='maize',
                 style={'width': "40%"}
                 ),

    html.Br(),

    dcc.Graph(id='commodity_prices', animate=True, style={"backgroundColor": "#1a2d46", 'color': '#ffffff'})

])