# Code creating a dashboard using plotly.dash

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from startupjh.data import scraper_api

app = dash.Dash(__name__)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

df = scraper_api("automation+container+terminal")

fig = px.bar(df, x="year", y="citations", barmode="group")

fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)
fig.update_xaxes(range=[1990, 2025])

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(children='Topic: Automation container terminal',
            style={
            'textAlign': 'center',
            'color': colors['text']
        }),

    html.Div(children='''
        Total number of citations per year
    ''', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)