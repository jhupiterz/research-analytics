# Code creating a dashboard using plotly.dash

from startupjh.data_collection import consolidated_df
from startupjh import plots
from startupjh.data_preprocessing import data_cleaning, data_enrichment

import time
import dash
import dash_cytoscape as cyto
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Execution timer ------------------------------------------
start_time = time.time()

# Data loading and cleaning - takes a while... -------------
df, query = consolidated_df.get_consolidated_df()
df = data_cleaning.clean_df(df)
df = data_enrichment.get_citation_count(df)

# Dash app -------------------------------------------------

app = dash.Dash(__name__)

app.title = "Research Intelligence"

# App layout -----------------------------------------------
app.layout = html.Div([

    html.Div([
        html.Div([
            html.H3("research intelligence", style={'order': '2', 'color': 'darkblue'}),
            html.Img(src='/assets/ri-logo.png', style={'height': '70px', 'margin-right':'15px', 'order': '1'})],
            style = {'display': 'flex', 'flex-direction': 'row', 'align-items':'center', 'order': '1', 'flex-grow': '1'}),
        
        html.Div([
            html.H1(f"Topic: {query} ", style={'order': '3', 'color': 'darkblue', 'text-align': 'center'})],
            style = {'order': '2', 'flex-grow': '2'}),
        
        html.Div([
            html.H5(f"execution time: {time.time() - start_time} seconds", style={'order': '1', 'color': 'darkblue', 'text-align': 'right'})],
            style = {'order': '3', 'flex-grow': '1'})],
             
        style = {'width': '95%', 'margin': 'auto', 'height': '10%', 'display': 'flex', 'flex-direction': 'row', 'align-items':'center', 'justify-content': 'space-between'}),

    html.Br(),
    html.Br(),
    
    html.Div([
        html.Div([
            html.H2("Earliest publication in", style={'color': 'darkblue'}),
            html.H1(f"{df.published_year.min()}", style={'color': 'darkblue'})],
            style={'width': '20%', 'height': '10%', 'order': '1', 'display': 'flex',
                   'flex-direction': 'column', 'align-items':'center', 'backgroundColor': '#E2D1F9'}),

        html.Div([
            html.H2("Latest publication in", style={'color': 'darkblue'}),
            html.H1(f"{df.published_year.max()}", style={'color': 'darkblue'})],
            style={'width': '20%', 'height': '10%', 'order': '3', 'display': 'flex',
                   'flex-direction': 'column', 'align-items': 'center', 'backgroundColor': '#E2D1F9'}),

        html.Div([
            html.H2("Top publisher", style={'color': 'darkblue'}),
            html.P(f"{plots.get_top_publisher(df)}", style = {'font-size': '1vw', 'color': 'darkblue'})],
            style={'width': '30%', 'height': '10%', 'order': '2', 'display': 'flex',
                   'flex-direction': 'column', 'align-items': 'center', 'backgroundColor': '#E2D1F9'})
    ], style = {'backgroundColor':'#E2D1F9','width': '95%', 'display': 'flex', 'margin': 'auto',
                'flex-direction': 'row', 'align-items': 'center', 'justify-content': 'space-between'}),
    
    html.Br(),
    html.Br(),
    
    html.Div([
        html.Div([
            dcc.Graph(
                id='keywords_graph',
                figure=plots.make_top_key_words(df, query),
                style = {'order': '1', 'backgroundColor': '#E2D1F9'}
            ),
            dcc.Graph(
                    id='accessibility_pie',
                    figure=plots.make_access_pie(df),
                    style = {'order': '2', 'backgroundColor': '#E2D1F9'}
                ),
            ], style={'backgroundColor': '#E2D1F9', 'width': '95%', 'display': 'flex',
                    'flex-direction': 'row', 'align-items': 'center', 'margin' : 'auto',
                    'margin-top': '25px','justify-content': 'space-evenly'}),
        
        html.Br(),
        html.Br(),
        
        html.Div([
            dcc.Graph(
                    id='publication_graph',
                    figure=plots.make_pub_per_year(df),
                    style = {'order' : '1', 'backgroundColor': '#E2D1F9'}
            ),
            dcc.Graph(
                    id='citations_graph',
                    figure=plots.make_citations_per_year(df),
                    style = {'order': '2', 'backgroundColor': '#E2D1F9'}
            ),
        ], style={'backgroundColor': '#E2D1F9', 'width': '95%', 'display': 'flex',
                'flex-direction': 'row', 'align-items': 'center', 'margin': 'auto',
                'margin-bottom': '25px', 'justify-content': 'space-evenly'})],
        
        style = {'backgroundColor': '#E2D1F9', 'width': '95%', 'display': 'flex',
                'flex-direction': 'column', 'align-items': 'center', 'margin': 'auto',
                'justify-content': 'space-evenly'}),
    
    html.Br(),
    html.Br(),
    
    html.Div([
    html.H2("Collaboration network", style = {'font-size': '22px', 'font-family': 'Courier New, monospace',
                                              'color': 'darkblue'}),
    cyto.Cytoscape(
        id='cytoscape',
        elements= plots.generate_graph_elements(df),
        layout={'name': 'circle'},
        stylesheet = [
            {
                'selector': 'label',
                'style': {
                    'content': 'data(label)',
                    'color': 'black',
                    'background-color': '#317773'
                }
            },
            {
                'selector': 'node',
                'style': {
                    'label': 'data(label)'
                } 
            },
            {
                'selector': '.author',
                'style': {
                    'background-color': '#317773'
                }
            },
            {
                'selector': '.collaboration',
                'style': {
                    'line-color': 'grey'
                }
            }
            ])],
        
    style = {'backgroundColor': '#E2D1F9',
             'width': '95%', 'margin': 'auto', 'margin-bottom': '20px',
             'display': 'flex', 'flex-direction': 'column', 'align-items': 'center'})

], style = {'backgroundColor': '#E2D1F9'})

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)