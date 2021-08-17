# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import os

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SKETCHY])
server = app.server

COL_1_content = html.Div([
    html.H1("Description"),
    dcc.Markdown('''
    This project uses Natural Language Processing and Machine Learning methods to achieve multi-class classification problem.
    In this project, I use approximately ten-thousand descriptions of podcasts broadcasting in Spotify which are obtained by API. 
    Together with their associated label, the data is used to trained the models to classify the label from text. 
    All the labels are pre-defined by me, currently 10 classes, including `["machine learning", "cooking", "crime", "politics", "kid", "comedy", "sport", "culture", "lifestyle", "business"]`
    ''')
])

COL_2_content = html.Div([
    dcc.Input(id='input-1-state', type='text', value='Montréal'),
    dcc.Input(id='input-2-state', type='text', value='Canada'),
    html.Button(id='submit-button-state', n_clicks=0, children='Submit'),
    html.Div(id='output-state')
],
style={
    'text-align':'center',
    'align-items': 'center',
    'transform': 'translate(0%, 50%)'
})

COL_3_content = html.Div([
    html.H4("Result", className="card-header"),
    dcc.Markdown("{cooking: 0.45, ...}", className="card-text", id="result-holder"),
], className="card border-primary mb-3")


app.layout = html.Div([
    html.Nav(html.A("Topic modelling", className="navbar-brand"), className="navbar navbar-expand-lg navbar-dark bg-primary"),
    dbc.Row([
        dbc.Col(COL_1_content),
        dbc.Col(COL_2_content),
        dbc.Col(COL_3_content)
    ]),
    
])



@app.callback(Output('output-state', 'children'),
              Output('result-holder', 'children'),
              Input('submit-button-state', 'n_clicks'),
              State('input-1-state', 'value'),
              State('input-2-state', 'value'))
def update_output(n_clicks, input1, input2):
    return '''
        The Button has been pressed {} times,
        Input 1 is "{}",
        and Input 2 is "{}"
    '''.format(n_clicks, input1, input2), f'''
    - input1 : {input1} \n - input2 : {input2}
    '''


if __name__ == '__main__':
    app.run_server(debug=False, port=os.getenv('PORT','8050'))
