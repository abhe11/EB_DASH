import dash
import plotly
import dash_core_components as dcc
import dash_html_components as html 
import dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import os as os

from app import app
import tab1 
import tab2 
import sidepanel 
import transforms

import sqlite3
import dash
from dash.dependencies import Input, Output
import dash_table
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
app.layout = sidepanel.layout

@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return tab1.layout
    elif tab == 'tab-2':
       return tab2.layout


operators = [['ge ', '>='],
             ['le ', '<='],
             ['lt ', '<'],
             ['gt ', '>'],
             ['ne ', '!='],
             ['eq ', '='],
             ['contains '],
             ['datestartswith ']]


def split_filter_part(filter_part):
    for operator_type in operators:
        for operator in operator_type:
            if operator in filter_part:
                
                name_part, value_part = filter_part.split(operator, 1)
                name = name_part[name_part.find('{') + 1: name_part.rfind('}')]

                value_part = value_part.strip()
                v0 = value_part[0]
                if (v0 == value_part[-1] and v0 in ("'", '"', '`')):
                    value = value_part[1: -1].replace('\\' + v0, v0)
                else:
                    try:
                        value = float(value_part)
                    except ValueError:
                        value = value_part

                # word operators need spaces after them in the filter string,
                # but we don't want these later
                return name, operator_type[0].strip(), value

    return [None] * 3


@app.callback(
    [Output('table-sorting-filtering', 'data'),
    Output('qty' , 'children')],
      [Input('table-sorting-filtering', "page_current")
     , Input('table-sorting-filtering', "page_size")
     , Input('table-sorting-filtering', 'sort_by')
     , Input('table-sorting-filtering', 'filter_query')
     , Input('rating-95', 'value')
     , Input('price-slider', 'value')
     , Input('month-slider', 'value')
     , Input('day-slider', 'value')
     , Input('supplier', 'value')
     ])
def update_table(page_current, page_size, sort_by, filter1, ratingcheck, prices ,month, day, supplier):
    filtering_expressions = filter1.split(' && ')
    dff = transforms.df
    print(ratingcheck)

    low = prices[0]
    high = prices[1]

    jan=month[0]
    dec=month[1]
    
    mind=day[0]
    maxd=day[1]
    
    dff1=[]
    
    if 'All' in supplier :
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
        dff = dff.loc[dff['C'] >= 14]
    else:
        dff

    for filter_part in filtering_expressions:
        col_name, operator, filter_value = split_filter_part(filter_part)

        if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
            # these operators match pandas series operator method names
            dff = dff.loc[getattr(dff[col_name], operator)(filter_value)]
        elif operator == 'contains':
            dff = dff.loc[dff[col_name].str.contains(filter_value)]
        elif operator == 'datestartswith':
            # this is a simplification of the front-end filtering logic,
            # only works with complete fields in standard format
            dff = dff.loc[dff[col_name].str.startswith(filter_value)]

    if len(sort_by):
        dff = dff.sort_values(
            [col['column_id'] for col in sort_by],
            ascending=[
                col['direction'] == 'asc'
                for col in sort_by
            ],
            inplace=False
        )

    page = page_current
    size = page_size
    
    dff=dff.drop(['A','B','C'], axis=1)
                 
    return dff.iloc[page * size: (page + 1) * size].to_dict('records'),dff['QUANTITY'].sum()

    

if __name__ == '__main__':
  #port = int(os.environ.get('PORT', 5000))
  #app.run_server(host='0.0.0.0',port = port,debug=True)
  app.run_server(debug=True)
 
