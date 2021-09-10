# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import os
import dash_table
from utils import *


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LITERA])
server = app.server

modelsName = {
    'model_2' : "Sequential",
    'fineTune' : "Fine-tuned Distilled BERT"
}
initial_fig = get_initial_fig()

COL_1_content = html.Div([
    html.H1("Description"),
    html.P('''
    This project uses Natural Language Processing and Machine Learning methods to achieve multi-class classification problem.
    In this project, I use approximately ten-thousand descriptions of podcasts broadcasting in Spotify which are collected by API. 
    Together with their associated label, the data is used to trained the models to classify the label from text. 
    All the labels are pre-defined by me, currently 10 classes, including 
    ''', style={'font-weight': '400', 'font-size':'large'}, className='lead'),
    html.Code('"machine learning", "cooking", "crime", "politics", "kid", "comedy", "sport", "culture", "lifestyle", "business"')
], className="col", id='col1')


COL_2_content = html.Div([
    html.Div([
        dcc.Textarea(className="form-control", id="input-text-area", rows="10", placeholder='Type input here')
    ]),
    html.Div([
        dcc.Dropdown(options=[
                        {'label': 'Sequential model', 'value': 'model_2'},
                        {'label': 'Fine-tuned Distilled BERT', 'value': 'fineTune'}
                    ], searchable=False, placeholder="Select the model", id='model_selection', clearable=False),
    ]),
    html.Div([
        html.Button(id='submit-button-state', n_clicks=0, children='Submit', className="btn btn-lg btn-primary", style={"margin":"10px"}),
        html.Div(id='output-state', children='output here')
    ])
],
style={
    'text-align':'center',
    'align-items': 'center',
}, className='col', id='col2')

COL_3_content = html.Div([
    html.H4("Result"),
    dcc.Graph(id='result-fig', figure=initial_fig),
], className='col', id='col3')


app.layout = html.Div([
    html.Nav(html.A("Topic modelling", className="navbar-brand"), className="navbar navbar-expand-lg navbar-dark bg-primary"),
    dbc.Row([
        dbc.Col(COL_1_content),
        dbc.Col(COL_2_content),
        dbc.Col(COL_3_content),
    ]),
])


@app.callback(Output('output-state', 'children'),
              Output('result-fig', 'figure'),
              Input('submit-button-state', 'n_clicks'),
              State('model_selection', 'value'),
              State('input-text-area', 'value'))
def update_output(n_clicks, selected_model, text):
    if text is None: 
        return "Please give the input", initial_fig
    if selected_model is None:
        return "Please select the model", initial_fig
    print(f'selected model: {selected_model}')
    print(f'input text: {text}')
    out = '''Using {} model'''.format(modelsName[selected_model])
    if n_clicks>0:
        out+= '''\nPlease wait for the result'''
    result_df = send_request(model=selected_model, text=preprocess(text))
    result_fig = px.pie(result_df, values='probabilities', names='label', title='Labels probabilities')
    return out, result_fig


if __name__ == '__main__':
    app.run_server(debug=False, port=os.getenv('PORT','8050'))
    hello = requests.get(f"http://{INGRESS_URL}/topicmodelling").text
    print(hello)
