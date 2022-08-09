######### Import your libraries #######
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly as py
import plotly.graph_objs as go


###### Define your variables #####
tabtitle = 'Video Games Sales'
color1='#92A5E8'
color2='#8E44AD'
color3='#FFC300'
sourceurl = 'https://www.kaggle.com/datasets/gregorut/videogamesales'
githublink = 'https://github.com/vkhvan/304-titanic-dropdown'


###### Import a dataframe #######
df = pd.read_csv("https://github.com/vkhvan/304-titanic-dropdown/blob/main/data/vgsales.csv")
##df['Female']=df['Sex'].map({'male':0, 'female':1})
##df['Cabin Class'] = df['Pclass'].map({1:'first', 2: 'second', 3:'third'})
df = df[(df.Year>2005.0) & (df.Year<2010.0) & ((df.Platform == 'Wii') | (df.Platform == 'PS2') | (df.Platform == 'X360'))]
variables_list=['NA_Sales', 'EU_Sales', 'JP_Sales', 'Global_Sales']

########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

####### Layout of the app ########
app.layout = html.Div([
    html.H3('Choose a continuous variable for summary statistics:'),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in variables_list],
        value=variables_list[0]
    ),
    html.Br(),
    dcc.Graph(id='display-value'),
    html.A('Code on Github', href=githublink),
    html.Br(),
    html.A("Data Source", href=sourceurl),
])


######### Interactive callbacks go here #########
@app.callback(Output('display-value', 'figure'),
              [Input('dropdown', 'value')])
def display_value(continuous_var):
    grouped_sum=df.groupby(['Platform', 'Year'])[continuous_var].sum()
    results=pd.DataFrame(grouped_sum)
    
    # Create a grouped bar chart
    mydata1 = go.Bar(
    x=results.loc['PS2'].index,
    y=results.loc['PS2'][continuous_var],
    name='PS2',
    marker=dict(color='darkgreen')
    )
    mydata2 = go.Bar(
    x=results.loc['X360'].index,
    y=results.loc['X360'][continuous_var],
    name='X360',
    marker=dict(color='lightblue')
    )
    mydata3 = go.Bar(
    x=results.loc['Wii'].index,
    y=results.loc['Wii'][continuous_var],
    name='Wii',
    marker=dict(color='orange')
    )

    mylayout = go.Layout(
    title='Grouped bar chart',
    xaxis = dict(title = 'Year'), # x-axis label
    yaxis = dict(title = str(continuous_var)), # y-axis label

    )
    fig = go.Figure(data=[mydata1, mydata2, mydata3], layout=mylayout)
    return fig


######### Run the app #########
if __name__ == '__main__':
    app.run_server(debug=True)
