import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import dash
from dash.dependencies import Input, Output
import dash_table
import pandas as pd


df = pd.read_csv(r'master.csv')

df = df[['S_NO', 'NAME_OF_THE_VESSEL', 'QUANTITY', 'DISCHARGE_COMPLETED', 'PORT',
       'pono', 'SUPPLIER', 'A', 'B', 'C']]

df['DISCHARGE_COMPLETED']=df['A'].astype(str)+'-'+df['B'].astype('str')+'-'+df['C'].astype('str')
df['DISCHARGE_COMPLETED']=pd.to_datetime(df['DISCHARGE_COMPLETED'],format='%d-%m-%y')
df['DISCHARGE_COMPLETED']=df['DISCHARGE_COMPLETED'].dt.date
df['QUANTITY']=pd.to_numeric(df['QUANTITY'])
df['A']=pd.to_numeric(df['A'])
df['B']=pd.to_numeric(df['B'])
df['C']=pd.to_numeric(df['C'])

l=df['SUPPLIER']
    
for i in range(len(l)):
    l[i] = l[i].replace("_", " ")
    l[i] = l[i].replace("/", "")
    l[i] = l[i].upper()
