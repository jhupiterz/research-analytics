# Code creating a dashboard using plotly.dash

from startupjh.data_collection import consolidated_df
from startupjh import plots
from startupjh.data_preprocessing import data_cleaning, data_enrichment

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Data loading and cleaning - takes a while...
df = consolidated_df.get_consolidated_df()
df = data_cleaning.clean_df(df)
df = data_enrichment.get_citation_count(df)
print(df.columns)

# Dash app

app = dash.Dash(__name__)

app.title = "Research Intelligence"

# App layout
app.layout = html.Div([

    html.H1("research intelligence", style={'text-align': 'center'}),

    html.Br(),
    
    html.Div([
        html.Div([
            dcc.Graph(
                id='first_pub_box',
                figure=plots.make_first_pub_box(df)
            )], style={'width': '30%', 'height': '10%', 'display': 'inline-block'}),

        html.Div([
            dcc.Graph(
                id='latest_pub_box',
                figure=plots.make_latest_pub_box(df)
            )], style={'width': '30%', 'height': '10%', 'display': 'inline-block'}),

        html.Div([
            dcc.Graph(
                id='top_pub_box',
                figure=plots.make_top_pub_box()
            )], style={'width': '30%', 'height': '10%', 'display': 'inline-block'})
    ], style = {'backgroundColor':'#d8b3ff','width': '100%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center', "margin-bottom": "100px"}),
    
    html.Div([
        dcc.Graph(
            id='keywords_graph',
            figure=plots.make_top_key_words(df)
        ),
        dcc.Graph(
                id='publication_graph',
                figure=plots.make_pub_per_year(df)
            ),
        ], style={'backgroundColor': '#d1d1d1', 'width': '45%', 'display': 'inline-block', "margin-bottom": "100px"}),
    
    html.Div([
        dcc.Graph(
                id='accessibility_pie',
                figure=plots.make_access_pie(df)
        ),
        dcc.Graph(
                id='citations_graph',
                figure=plots.make_citations_per_year(df)
        ),
    ], style={'backgroundColor': '#d1d1d1', 'width': '45%', 'display': 'inline-block', "margin-bottom": "100px"})

])

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)



