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
            html.H3("research intelligence", style={'order': '2', 'color': 'grey'}),
            html.Img(src='/assets/ri-logo.png', style={'height': '70px', 'margin-right':'15px', 'order': '1'})],
            style = {'display': 'flex', 'flex-direction': 'row', 'align-items':'center', 'order': '1', 'flex-grow': '1'}),
        
        html.Div([
            html.H1(f"Topic: {query} ", style={'order': '3', 'text-align': 'center'})],
            style = {'order': '2', 'flex-grow': '2'}),
        
        html.Div([
            html.H5(f"execution time: {time.time() - start_time} seconds", style={'order': '1', 'color': 'grey', 'text-align': 'right'})],
            style = {'order': '3', 'flex-grow': '1'})],
             
        style = {'width': '95%', 'margin': 'auto', 'height': '10%', 'display': 'flex', 'flex-direction': 'row', 'align-items':'center', 'justify-content': 'space-between'}),

    html.Br(),
    html.Br(),
    
    html.Div([
        html.Div([
            html.H4("Research topic active since"),
            html.H1(f"{df.published_year.min()}")],
            style={'width': '20%', 'height': '10%', 'order': '1', 'display': 'flex',
                   'flex-direction': 'column', 'align-items':'center', 'backgroundColor': '#d8b3ff',
                   'border-widht': '2px', 'border-style': 'solid', 'border-color': 'black'}),

        html.Div([
            html.H4("Latest publication in"),
            html.H1(f"{df.published_year.max()}")],
            style={'width': '20%', 'height': '10%', 'order': '3', 'display': 'flex',
                   'flex-direction': 'column', 'align-items': 'center', 'backgroundColor': '#d8b3ff',
                   'border-widht': '2px', 'border-style': 'solid', 'border-color': 'black'}),

        html.Div([
            html.H4("Top publisher"),
            html.P(f"{plots.get_top_publisher(df)}", style = {'font-size': '1vw'})],
            style={'width': '30%', 'height': '10%', 'order': '2', 'display': 'flex',
                   'flex-direction': 'column', 'align-items': 'center', 'backgroundColor': '#d8b3ff',
                   'border-widht': '2px', 'border-style': 'solid', 'border-color': 'black'})
    ], style = {'backgroundColor':'white','width': '95%', 'display': 'flex', 'margin': 'auto',
                'flex-direction': 'row', 'align-items': 'center', 'justify-content': 'space-between'}),
    
    html.Br(),
    html.Br(),
    
    html.Div([
        html.Div([
            dcc.Graph(
                id='keywords_graph',
                figure=plots.make_top_key_words(df, query),
                style = {'order': '1', 'backgroundColor': '#d8b3ff'}
            ),
            dcc.Graph(
                    id='accessibility_pie',
                    figure=plots.make_access_pie(df),
                    style = {'order': '2', 'backgroundColor': '#d8b3ff'}
                ),
            ], style={'backgroundColor': '#d8b3ff', 'width': '95%', 'display': 'flex',
                    'flex-direction': 'row', 'align-items': 'center', 'margin' : 'auto',
                    'margin-top': '25px','justify-content': 'space-evenly'}),
        
        html.Br(),
        html.Br(),
        
        html.Div([
            dcc.Graph(
                    id='publication_graph',
                    figure=plots.make_pub_per_year(df),
                    style = {'order' : '1', 'backgroundColor': '#d8b3ff'}
            ),
            dcc.Graph(
                    id='citations_graph',
                    figure=plots.make_citations_per_year(df),
                    style = {'order': '2', 'backgroundColor': '#d8b3ff'}
            ),
        ], style={'backgroundColor': '#d8b3ff', 'width': '95%', 'display': 'flex',
                'flex-direction': 'row', 'align-items': 'center', 'margin': 'auto',
                'margin-bottom': '25px', 'justify-content': 'space-evenly'})],
        
        style = {'backgroundColor': '#d8b3ff', 'width': '95%', 'display': 'flex',
                'flex-direction': 'column', 'align-items': 'center', 'margin': 'auto',
                'border-widht': '2px', 'border-style': 'solid', 'border-color': 'black',
                'justify-content': 'space-evenly'}),
    
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