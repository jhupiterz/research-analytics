# Code creating a dashboard using plotly.dash

from startupjh.data_collection import consolidated_df
from startupjh import plots
from startupjh.data_collection import semantic_api
from startupjh.data_preprocessing import data_cleaning, data_enrichment

import time
import dash
import dash_cytoscape as cyto
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Execution timer ------------------------------------------
start_time = time.time()

# Data loading and cleaning whith OTHER APIs (DOAJ, CORE, GoogleScholar, Unpaywall) ---
# df, query = consolidated_df.get_consolidated_df()
# df = data_cleaning.clean_df(df)
# df = data_enrichment.get_citation_count(df)

# Data loading and cleaning with SEMANTIC_SCHOLAR API
df, all_references_df, total_results, query = semantic_api.get_all_results_from_semantic_scholar()

# Dash app -------------------------------------------------

app = dash.Dash(
    __name__, suppress_callback_exceptions = True,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}])

app.title = "Research Intelligence"

# App layout -----------------------------------------------
app.layout = html.Div([
    
    html.Br(),
    html.Br(),
    
    html.Div([
        html.Div([
            html.H3("research intelligence", style={'order': '2', 'color': 'white'}),
            html.Img(src='/assets/maze.png', style={'height': '70px', 'margin-right':'15px', 'order': '1'})],
            style = {'display': 'flex', 'flex-direction': 'row', 'align-items':'center', 'order': '1', 'flex-grow': '1'}),
        
        html.Div([
            html.H1(f"Topic: {query} ", style={'order': '3', 'color': 'white', 'text-align': 'center'})],
            style = {'order': '2', 'flex-grow': '2'}),
        
        html.Div([
            html.H5(f"execution time: {time.time() - start_time} seconds", style={'order': '1', 'color': 'white',
                                                                                  'text-align': 'right'})],
            style = {'order': '3', 'flex-grow': '1'})],
             
        style = {'width': '95%', 'margin': 'auto', 'height': '10%', 'display': 'flex', 'flex-direction': 'row', 'align-items':'center', 'justify-content': 'space-between'}),
    
    html.Div([ html.A('Results powered by Semantic Scholar', href = "https://www.semanticscholar.org/", target = '_blank', style = {'color': 'white'})], style = {'margin': 'auto', 'width': '100%', 'height':'5%', 'text-align':' center'}),

    html.Br(),
    html.Br(),
    html.Br(),
    
    html.Div([
    dcc.Tabs(id="tabs-example-graph", value='tab-1-example-graph', children=[
        dcc.Tab(label='Search results', value='tab-1-example-graph',
                style = {'order': '1', 'background-color': 'white', 'font-weight': 'bold'},
                selected_style = {'order': '1', 'background-color': '#eda109', 'font-weight': 'bold', 'width': '100%'}),
        dcc.Tab(label='Reference landscape', value='tab-2-example-graph',
                style = {'order': '2', 'background-color': 'white', 'font-weight': 'bold', 'width': '100%'},
                selected_style = {'order': '2', 'background-color': '#eda109', 'font-weight': 'bold', 'width': '100%'}),
        dcc.Tab(label='Networks', value='tab-3-example-graph',
                style = {'order': '3', 'background-color': 'white', 'font-weight': 'bold', 'width': '100%'},
                selected_style = {'order': '3', 'background-color': '#eda109', 'font-weight': 'bold', 'width': '100%'})
        ])], style = {'backgroundColor': '#101126', 'width': '95%', 'height': '10%', 'display': 'flex',
                      'flex-direction': 'row', 'margin' : 'auto', 'align-items': 'center'}),
    
    html.Br(),
    html.Br(),
    
    html.Div(id='tabs-content-example-graph')],
    style = {'backgroundColor': '#18192e', 'margin-bottom': '15px'})

@app.callback(Output('tabs-content-example-graph', 'children'),
              Input('tabs-example-graph', 'value'))
def render_content(tab):
    if tab == 'tab-1-example-graph':
        return html.Div([
            html.Div([
        html.Div([
            html.H2("Earliest publication in", style={'color': '#eda109', 'font-family': 'Courier New, monospace'}),
            html.H1(f"{int(df.year.min())}", style={'color': 'white', 'font-family': 'Courier New, monospace'})],
            style={'width': '20%', 'height': '10%', 'order': '1', 'display': 'flex',
                   'flex-direction': 'column', 'align-items':'center', 'backgroundColor': '#101126'}),

        html.Div([
            html.H2("Latest publication in", style={'color': '#eda109', 'font-family': 'Courier New, monospace'}),
            html.H1(f"{int(df.year.max())}", style={'color': 'white', 'font-family': 'Courier New, monospace'})],
            style={'width': '20%', 'height': '10%', 'order': '3', 'display': 'flex',
                   'flex-direction': 'column', 'align-items': 'center', 'backgroundColor': '#101126'}),

        html.Div([
            html.H2("Total results", style={'color': '#eda109', 'font-family': 'Courier New, monospace'}),
            html.H1(f"{total_results}", style = {'color': 'white', 'font-family': 'Courier New, monospace'})],
            style={'width': '30%', 'height': '10%', 'order': '2', 'display': 'flex',
                   'flex-direction': 'column', 'align-items': 'center', 'backgroundColor': '#101126'})
    ], style = {'backgroundColor':'#101126','width': '95%', 'display': 'flex', 'margin': 'auto',
                'flex-direction': 'row', 'align-items': 'center', 'justify-content': 'space-around'}),
    
    html.Br(),
    html.Br(),
    
    html.Div([
        html.Div([
            dcc.Graph(
                id='keywords_graph',
                figure=plots.make_top_key_words(df, query),
                style = {'order': '1', 'backgroundColor': '#101126'}
            ),
            dcc.Graph(
                    id='accessibility_pie',
                    figure=plots.make_access_pie(df, 'semantic_scholar'),
                    style = {'order': '2', 'backgroundColor': '#101126'}
                ),
            ], style={'backgroundColor': '#101126', 'width': '95%', 'display': 'flex',
                    'flex-direction': 'row', 'align-items': 'center', 'margin' : 'auto',
                    'margin-top': '25px','justify-content': 'space-evenly'}),
        
        html.Br(),
        html.Br(),
        
        html.Div([
            dcc.Graph(
                    id='publication_graph',
                    figure=plots.make_pub_per_year_line(df),
                    style = {'order' : '1', 'backgroundColor': '#101126'}
            ),
            dcc.Graph(
                    id='citations_graph',
                    figure=plots.make_citations_per_year_line(df),
                    style = {'order': '2', 'backgroundColor': '#101126'}
            ),
        ], style={'backgroundColor': '#101126', 'width': '95%', 'display': 'flex',
                'flex-direction': 'row', 'align-items': 'center', 'margin': 'auto',
                'margin-bottom': '25px', 'justify-content': 'space-evenly'}),
        
        html.Br(),
        html.Br(),
        
        html.Div([
            dcc.Graph(
                    id='fields_pie',
                    figure=plots.make_fields_pie(df),
                    style = {'order' : '1', 'backgroundColor': '#101126'}
            ),
            dcc.Graph(
                    id='citations_graph',
                    figure=plots.make_active_authors(df),
                    style = {'order': '2', 'backgroundColor': '#101126'}
            ),
        ], style={'backgroundColor': '#101126', 'width': '95%', 'display': 'flex',
                'flex-direction': 'row', 'align-items': 'center', 'margin': 'auto',
                'margin-bottom': '25px', 'justify-content': 'space-evenly'})
        ],
        
        style = {'backgroundColor': '#101126', 'width': '95%', 'display': 'flex',
                'flex-direction': 'column', 'align-items': 'center', 'margin': 'auto',
                'justify-content': 'space-evenly'}),
    ])
    if tab == 'tab-2-example-graph':
        return html.Div([
            html.Div([
        html.Div([
            html.H2("Earliest publication in", style={'color': '#eda109', 'font-family': 'Courier New, monospace'}),
            html.H1(f"{int(all_references_df.year.min())}", style={'color': 'white', 'font-family': 'Courier New, monospace'})],
            style={'width': '20%', 'height': '10%', 'order': '1', 'display': 'flex',
                   'flex-direction': 'column', 'align-items':'center', 'backgroundColor': '#101126'}),

        html.Div([
            html.H2("Latest publication in", style={'color': '#eda109', 'font-family': 'Courier New, monospace'}),
            html.H1(f"{int(all_references_df.year.max())}", style={'color': 'white', 'font-family': 'Courier New, monospace'})],
            style={'width': '20%', 'height': '10%', 'order': '3', 'display': 'flex',
                   'flex-direction': 'column', 'align-items': 'center', 'backgroundColor': '#101126'}),

        html.Div([
            html.H2("Total results", style={'color': '#eda109', 'font-family': 'Courier New, monospace'}),
            html.H1(f"{total_results}", style = {'color': 'white', 'font-family': 'Courier New, monospace'})],
            style={'width': '30%', 'height': '10%', 'order': '2', 'display': 'flex',
                   'flex-direction': 'column', 'align-items': 'center', 'backgroundColor': '#101126'})
    ], style = {'backgroundColor':'#101126','width': '95%', 'display': 'flex', 'margin': 'auto',
                'flex-direction': 'row', 'align-items': 'center', 'justify-content': 'space-around'}),
    
    html.Br(),
    html.Br(),
    
    html.Div([
        html.Div([
            dcc.Graph(
                id='keywords_graph',
                figure=plots.make_top_key_words(all_references_df, query),
                style = {'order': '1', 'backgroundColor': '#101126'}
            ),
            dcc.Graph(
                    id='accessibility_pie',
                    figure=plots.make_access_pie(all_references_df, 'semantic_scholar'),
                    style = {'order': '2', 'backgroundColor': '#101126'}
                ),
            ], style={'backgroundColor': '#101126', 'width': '95%', 'display': 'flex',
                    'flex-direction': 'row', 'align-items': 'center', 'margin' : 'auto',
                    'margin-top': '25px','justify-content': 'space-evenly'}),
        
        html.Br(),
        html.Br(),
        
        html.Div([
            dcc.Graph(
                    id='publication_graph',
                    figure=plots.make_pub_per_year_line(all_references_df),
                    style = {'order' : '1', 'backgroundColor': '#101126'}
            ),
            dcc.Graph(
                    id='citations_graph',
                    figure=plots.make_citations_per_year_line(all_references_df),
                    style = {'order': '2', 'backgroundColor': '#101126'}
            ),
        ], style={'backgroundColor': '#101126', 'width': '95%', 'display': 'flex',
                'flex-direction': 'row', 'align-items': 'center', 'margin': 'auto',
                'margin-bottom': '25px', 'justify-content': 'space-evenly'}),
        
        html.Br(),
        html.Br(),
        
        html.Div([
            dcc.Graph(
                    id='fields_pie',
                    figure=plots.make_fields_pie(all_references_df),
                    style = {'order' : '1', 'backgroundColor': '#101126'}
            ),
            dcc.Graph(
                    id='most_active_authors',
                    figure=plots.make_active_authors(all_references_df),
                    style = {'order': '2', 'backgroundColor': '#101126'}
            ),
        ], style={'backgroundColor': '#101126', 'width': '95%', 'display': 'flex',
                'flex-direction': 'row', 'align-items': 'center', 'margin': 'auto',
                'margin-bottom': '25px', 'justify-content': 'space-evenly'})
        ],
        
        style = {'backgroundColor': '#101126', 'width': '95%', 'display': 'flex',
                'flex-direction': 'column', 'align-items': 'center', 'margin': 'auto',
                'justify-content': 'space-evenly'}),
    ])
    if tab == 'tab-3-example-graph':
        return html.Div([
        html.Div([
        html.H2("Collaboration network", style = {'font-size': '22px', 'font-family': 'Courier New, monospace',
                                                'color': 'white'}),
        cyto.Cytoscape(
            id='cytoscape',
            elements= plots.generate_graph_elements_collab(df),
            layout={'name': 'circle'},
            stylesheet = [
                {
                    'selector': 'label',
                    'style': {
                        'content': 'data(label)',
                        'color': 'white',
                        'background-color': '#eda109'
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
                        'background-color': '#eda109'
                    }
                },
                {
                    'selector': '.collaboration',
                    'style': {
                        'line-color': 'lightgrey'
                    }
                }
                ])],
            
        style = {'order': '1', 'backgroundColor': '#101126',
                'width': '95%', 'margin': 'auto', 'margin-bottom': '20px',
                'display': 'flex', 'flex-direction': 'column', 'align-items': 'center'}),
        
        html.Br(),
        html.Br(),
        
        html.Div([
        html.H2("Citation network", style = {'font-size': '22px', 'font-family': 'Courier New, monospace',
                                                'color': 'white'}),
        cyto.Cytoscape(
            id='cytoscape-event-callbacks-1',
            elements= plots.generate_graph_elements_network(all_references_df, df),
            layout={'name': 'cose', 'height': '80%', 'width': '75%'},
            style={'width': '100%', 'height': '1200px'},
            stylesheet = [
                {
                    'selector': 'node',
                    'style': {
                        #'label': ''
                    } 
                },
                {
                    'selector': '.res',
                    'style': {
                        'background-color': '#eda109',
                        'label': 'data(label)',
                        'color': '#eda109',
                        'height': '12px',
                        'width': '12px'
                    }
                },
                {
                    'selector': '.ref',
                    'style': {
                        'background-color': 'white',
                        'color': 'white',
                        'height': '7px',
                        'width': '7px'
                    }
                },
                {
                    'selector': '.citation',
                    'style': {
                        'line-color': 'grey',
                        'width': 0.5
                    }
                }
                ])],
            
        style = {'order': '2', 'backgroundColor': '#101126',
                'width': '95%', 'height': '1800px', 'margin': 'auto', 'margin-bottom': '20px',
                'display': 'flex', 'flex-direction': 'column', 'align-items': 'center'})],
        
        style = {'backgroundColor': '#101126',
                'width': '95%', 'height': '2700px', 'margin': 'auto', 'margin-bottom': '20px',
                'display': 'flex', 'flex-direction': 'column', 'align-items': 'center'})

@app.callback(Output('cytoscape-event-callbacks-1', 'stylesheet'),
              Input('cytoscape-event-callbacks-1', 'mouseoverNodeData'))
def displayTapNodeData(data):
    if data:
        return [
                {
                    'selector': 'node',
                    'style': {
                        'label': 'data(label)'
                    } 
                },
                {
                    'selector': '.res',
                    'style': {
                        'background-color': '#eda109',
                        'label': 'data(label)',
                        'color': '#eda109',
                        'height': '12px',
                        'width': '12px'
                    }
                },
                {
                    'selector': '.ref',
                    'style': {
                        'background-color': 'white',
                        'color': 'white',
                        'height': '7px',
                        'width': '7px'
                    }
                },
                {
                    'selector': '.citation',
                    'style': {
                        'line-color': 'grey',
                        'width': 0.5
                    }
                }
                ]
    else:
        return [
                {
                    'selector': 'node',
                    'style': {
                        #'label': ''
                    } 
                },
                {
                    'selector': '.res',
                    'style': {
                        'background-color': '#eda109',
                        'label': 'data(label)',
                        'color': '#eda109',
                        'height': '12px',
                        'width': '12px'
                    }
                },
                {
                    'selector': '.ref',
                    'style': {
                        'background-color': 'white',
                        'color': 'white',
                        'height': '7px',
                        'width': '7px'
                    }
                },
                {
                    'selector': '.citation',
                    'style': {
                        'line-color': 'grey',
                        'width': 0.5
                    }
                }
                ]

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)