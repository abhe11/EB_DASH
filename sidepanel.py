import dash
import plotly
import dash_core_components as dcc
import dash_html_components as html 
import dash_bootstrap_components as dbc 
import dash_table
import pandas
from dash.dependencies import Input, Output

import app
import tab1
import tab2
import transforms

def BuildOptions(df, AddAll):  
    OptionList = [{'label': i, 'value': i} for i in df.unique()]
    if AddAll == 1:       
        OptionList.insert(0,{'label': 'All', 'value': 'All'})          
    return OptionList

df = transforms.df
min_p=df.C.min()
max_p=df.C.max()

min_m=df.B.min()
max_m=df.B.max()

min_d=df.A.min()
max_d=df.A.max()


options_array = BuildOptions(df.SUPPLIER,1)

layout = html.Div([
    html.H1('EB ')
    ,dbc.Row([dbc.Col(
        html.Div([
         html.H2('Filters')
        , dcc.Checklist(id='rating-95'
        , options = [
            {'label':'DISCHARGE_COMPLETED >= 2014 ', 'value':'Y'}
        ])
        ,html.Div([html.H5('Date Slider')
            ,dcc.RangeSlider(id='price-slider'
                            ,min = min_p
                            ,max= max_p
                            , marks = {14: '14',
                                        15: '15',
                                        16: '16',
                                        17: '17',
                                        18: '18',
                                        19: '19',
                                        20: '20',
                                       }
                            , value = [14,20]
                            )
                        
                            ]),
            html.Div([html.H5('Month Slider')
            ,dcc.RangeSlider(id='month-slider'
                            ,min = min_m
                            ,max= max_m
                            , marks = { 1:'1',
                                        2:'2',
                                        3:'3',
                                        4: '4',
                                        5: '5',
                                        6: '6',
                                        7: '7',
                                        8: '8',
                                        9: '9',
                                        10: '10',
                                       11:'11',
                                       12:'12',
                                       }
                            , value = [1,12]
                            )
                             
                              ]),
            html.Div([html.H5('Day Slider')
            ,dcc.RangeSlider(id='day-slider'
                            ,min = min_d
                            ,max= max_d
                            , marks = { 1:'1',
                                        3:'3',
                                        5: '5',
                                        7: '7',
                                        9: '9',
                                       11:'11',
                                       13:'13',
                                       15:'15',
                                       17:'17',
                                       19:'19',
                                       21:'21',
                                       23:'23',
                                       25:'25',
                                       27:'27',
                                       29:'29',
                                       31:'31',
                                       }
                            , value = [1,31]
                            )        
                        
                            ])
        ,html.Div([html.H5('Supplier')
            ,dcc.Dropdown(id='supplier'
                            ,options=options_array,
                            value='All',
                                multi=True
                            )],
                        className='two columns'
                            )

         ,html.Div(html.H5("QUANTITY(kgs)"))

            ,html.Div(
                                    id="qty",
                                    className="mini_container",
                                    style={"visibility": "visible"},
                                ),
                  
        ], style={'marginBottom': 50, 'marginTop': 25, 'marginLeft':15, 'marginRight':15})
    , width=3)

    ,dbc.Col(html.Div([
            dcc.Tabs(id="tabs", value='tab-1', children=[
                    dcc.Tab(label='Data Table', value='tab-1'),
                    dcc.Tab(label='Scatter Plot', value='tab-2'),
                ])
            , html.Div(id='tabs-content')
        ]), width=9)])
    
    ])
