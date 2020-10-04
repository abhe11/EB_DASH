import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc 
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import dash_table
from app import app
import transforms

df = transforms.df

layout = html.Div(
            id='table-paging-with-graph-container',
            className="five columns"
        )

@app.callback(Output('table-paging-with-graph-container', "children"),
    Output('qty' , 'children'),
[Input('rating-95', 'value')
, Input('price-slider', 'value')
, Input('month-slider', 'value')
, Input('day-slider', 'value') 
, Input('supplier', 'value')  
])

def update_graph(ratingcheck, prices ,month, day, supplier):
    dff = df

    low = prices[0]
    high = prices[1]

    jan=month[0]
    dec=month[1]
    
    mind=day[0]
    maxd=day[1]
    
    dff1=[]
    
    if 'All' in supplier:
        dff=transforms.df
    else:
        for i in supplier:
            dff = transforms.df
            if supplier=={'label': 'All', 'value': 'All'}:
    
                dff=dff
        
            else:
                dff1.append(dff.loc[(dff['SUPPLIER']==i)])
        dff = pd.concat(dff1)
    
    dff = dff.loc[(dff['C'] >= low) & (dff['C'] <= high)]
    
    dff = dff.loc[(dff['B'] >= jan) & (dff['B'] <= dec)]

    dff = dff.loc[(dff['A'] >= mind) & (dff['A'] <= maxd)]
    
    if ratingcheck == ['Y']:
       dff = dff.loc[dff['C'] >= 2014]
    else:
        dff

    trace1 = go.Scattergl(x = dff['DISCHARGE_COMPLETED']
                        , y = dff['QUANTITY']
                        , mode='markers'
                        , opacity=0.7
                        , marker={
                                'size': 8
                                , 'line': {'width': 0.5, 'color': 'white'}
                                }
                        , name='QUANTITY vs DISCHARGE_COMPLETED'
                    )
    return html.Div([
        dcc.Graph(
            id='rating-price'
            , figure={
                'data': [trace1
                    # dict(
                    #     x=df['price'],
                    #     y=df['rating'],
                    #     #text=df[df['continent'] == i]['country'],
                    #     mode='markers',
                    #     opacity=0.7,
                    #     marker={
                    #         'size': 8,
                    #         'line': {'width': 0.5, 'color': 'white'}
                    #     },
                    #     name='Price v Rating'
                    #) 
                ],
                'layout': dict(
                    xaxis={'title': 'DISCHARGE_COMPLETED'},
                    yaxis={'title': 'QUANTITY'},
                    margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                    legend={'x': 0, 'y': 1},
                    hovermode='closest'
                )
            }
        )
    ]),dff['QUANTITY'].sum()
