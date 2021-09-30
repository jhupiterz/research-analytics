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

df = pd.read_csv('papers.csv')

for template in "ggplot2":
    fig1 = px.bar(df, x="year", y="citations", barmode="group")

    fig1.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
    )
    fig1.update_xaxes(range=[1995, 2025])

for template in "ggplot2":
    fig2 = px.bar(df.groupby("year").count().reset_index(inplace=False), x="year", y="title", barmode="group")

    fig2.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
    )
    fig2.update_xaxes(range=[1995, 2025])

app.layout = html.Div([
    html.H1("Topic: automation container terminal"),
        html.Div(className="row",
                 children = [
                    html.Div(className= "six columns",
                    children = [
                        html.H3('Citations per year'),
                        html.Div(
                        dcc.Graph(id='fig1', figure=fig1)
            )]),

                    html.Div(className="six columns",
                    children = [
                        html.H3('Publications per year'),
                        html.Div(
                        dcc.Graph(id='fig2', figure=fig2)
            )]),
    ])
])

app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

if __name__ == '__main__':
    app.run_server(debug=True)