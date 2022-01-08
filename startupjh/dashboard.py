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
            html.H3("research intelligence", style={'order': '2', 'color': 'grey', 'margin-top': '30px'}),
            html.Img(src='/assets/ri-logo.png', style={'height': '70px', 'margin-left': '30px', 'margin-right':'15px', 'margin-top': '20px', 'order': '1'})],
            style = {'display': 'flex', 'flex-direction': 'row', 'align-items':'center', 'order': '1', 'flex-grow': '1'}),
        
        html.Div([
            html.H1(f"Topic: {query} ", style={'order': '3', 'margin-top': '30px', 'text-align': 'center'})],
            style = {'order': '2', 'flex-grow': '2'}),
        
        html.Div([
            html.H5(f"execution time: {time.time() - start_time} seconds", style={'order': '1', 'color': 'grey', 'margin-top': '30px', 'text-align': 'right', 'margin-right': '30px'})],
            style = {'order': '3', 'flex-grow': '1'})],
             
        style = {'width': '100%', 'height': '10%', 'display': 'flex', 'flex-direction': 'row', 'align-items':'center', 'justify-content': 'space-between'}),

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
                figure=plots.make_top_pub_box(df)
            )], style={'width': '30%', 'height': '10%', 'display': 'inline-block'})
    ], style = {'backgroundColor':'#d8b3ff','width': '100%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center', "margin-bottom": "100px"}),
    
    html.Div([
        dcc.Graph(
            id='keywords_graph',
            figure=plots.make_top_key_words(df, query)
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
    ], style={'backgroundColor': '#d1d1d1', 'width': '45%', 'display': 'inline-block', "margin-bottom": "100px"}),
    
    html.Div([
    html.P("Collaboration network:"),
    cyto.Cytoscape(
        id='cytoscape',
        elements= plots.generate_graph_elements(df),
        layout={'name': 'circle'}#,
        #style={'width': '2000px', 'height': '1000px'}
    )
    ])

])

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)