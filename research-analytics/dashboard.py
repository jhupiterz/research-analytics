#--------------------------------------------------------------------------#
#                   This code makes use of all other functions of          #
#                      the package to build a Dash Web App                 # 
#--------------------------------------------------------------------------#

# imports ------------------------------------------------------------------
import plots
from data_collection import semantic_api
from data_preprocessing import data_preprocess
import requests
import pandas as pd
import dash
import dash_cytoscape as cyto
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

# Data loading and cleaning with Semantic Scholar API -----------------------
#df, all_references_df, total_results, query = semantic_api.get_all_results_from_semantic_scholar()

# Instantiate Dash App ------------------------------------------------------

app = dash.Dash(
    __name__, suppress_callback_exceptions = True,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}])

app.title = "Research Intelligence"

# Build App layout ----------------------------------------------------------
app.layout = html.Div([
    
    html.Br(),
    html.Br(),
    
    # Top banner ------------------------------------------------------------
    html.Div([
        html.Div([
            html.H3("research intelligence", style={'order': '2', 'color': 'white'}),
            html.A(
                    href="https://jhupiterz.notion.site/Welcome-to-research-intelligence-a36796f418b040f6ade944f9c54e87cb",
                    target = '_blank',
                    children=[
                        html.Img(
                            alt="research intelligence",
                            src="/assets/maze.png",
                            style={'height': '70px', 'margin-right':'15px', 'order': '1'}
                        )
                    ]
                )],
            style = {'display': 'flex', 'flex-direction': 'row', 'align-items':'center', 'order': '1', 'width':'400px'}),
        
        html.Div([
            html.H1(id = 'topic', children = [], style={'color': 'white', 'text-align': 'center'})],
            style = {'order': '2', 'margin':'auto'}),
        
        html.Div([
            html.H5(f"Documentation", style={'order': '1', 'color': 'white', 'text-align': 'right'})],
            style = {'order': '3', 'width':'400px'})],
             
        style = {'width': '95%', 'margin': 'auto', 'height': '10%', 'display': 'flex', 'flex-direction': 'row', 'align-items':'center'}),
    
    # Credits to Semantic Scholar ---------------------------------------------
    html.Div([ html.A('Results powered by Semantic Scholar', href = "https://www.semanticscholar.org/", target = '_blank', style = {'color': 'white'})], style = {'margin': 'auto', 'width': '100%', 'height':'5%', 'text-align':' center'}),

    html.Br(),
    html.Br(),
    html.Br(),
    
    html.Div([
        html.Img(src='/assets/loupe.png', style={'height':'60px', 'order':'1', 'margin-right':'10px'}),
        dcc.Input(
            id='search-query',
            type = 'text',
            placeholder = 'insert your search keywords',
            debounce = True,
            spellCheck = True,
            inputMode = 'latin',
            name = 'text',
            autoFocus = False,
            minLength = 1, maxLength = 60,
            autoComplete='on',
            disabled = False,
            readOnly = False,
            size = '60',
            style = {'height': '100%', 'width': '30%', 'font-size': '20px', 'order':'2'})
        ], style = {'width': '95%', 'height':'50px', 'margin': 'auto', 'display':'flex',
                    'flex-direction':'row', 'align-items':'center', 'justify-content':'center'}),

    html.Br(),
    html.Br(),

    dcc.Store(id='store-initial-query-response', storage_type='memory'),
    dcc.Store(id='store-references-query-response', storage_type='memory'),
    
    html.Div(id = 'start-page', children = []),
    
    # # Tabs --------------------------------------------------------------------
    # html.Div([
    # dcc.Tabs(id="tabs-example-graph", style = {'width': '306%', 'height': '10%', 'align-items':'center'}, children=[
    #     dcc.Tab(label='Search results', value='tab-1-example-graph',
    #             style = {'order': '1', 'background-color': 'white', 'font-weight': 'bold'},
    #             selected_style = {'order': '1', 'background-color': '#eda109', 'font-weight': 'bold'}),
    #     dcc.Tab(label='Reference landscape', value='tab-2-example-graph',
    #             style = {'order': '2', 'background-color': 'white', 'font-weight': 'bold'},
    #             selected_style = {'order': '2', 'background-color': '#eda109', 'font-weight': 'bold'}),
    #     dcc.Tab(label='Networks', value='tab-3-example-graph',
    #             style = {'order': '3', 'background-color': 'white', 'font-weight': 'bold'},
    #             selected_style = {'order': '3', 'background-color': '#eda109', 'font-weight': 'bold'})
    #     ])], style = {'backgroundColor': '#101126', 'width': '95%', 'height': '10%', 'display': 'flex',
    #                   'flex-direction': 'row', 'margin' : 'auto', 'align-items': 'center'}),

    html.Br(),
    html.Br(),
    
    # # Tabs content generated by callbacks -------------------------------------
    # html.Div(id='tabs-content-example-graph'),
    
    #Bottom footer -----------------------------------------------------------
    html.Footer(html.P("Built by Scoollab using Plotly Dash", style = {'text-align':'center', 'color':'black'}),
                style = {'width': '100%', 'backgroundColor': '#eda109', 'vertical-align':'top'})],
    style = {'backgroundColor': '#18192e', 'padding-bottom': '5px'})

# Callbacks --------------------------------------------------------------------
# Store response of initial API query
@app.callback(
    Output('store-initial-query-response', 'data'),
    Input('search-query', 'value'))
def store_primary_data(value):
    #print(type(value))
    if value != None:
        url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={value}&limit=30&fields=url,title,abstract,authors,venue,year,referenceCount,citationCount,influentialCitationCount,isOpenAccess,fieldsOfStudy"
        response = requests.get(url).json()
        return response

# Store dictionary of references of all initial papers
@app.callback(
    Output('store-references-query-response', 'data'),
    Input('store-initial-query-response', 'data'))
def store_references_data(data):
    if data != None:
        ref_dict = []
        for paper in data['data']:
            paper_id = paper['paperId']
            url = f"https://api.semanticscholar.org/graph/v1/paper/{paper_id}/references?limit=50&fields=intents,isInfluential,paperId,url,title,abstract,venue,year,referenceCount,citationCount,influentialCitationCount,isOpenAccess,fieldsOfStudy,authors"
            response = requests.get(url).json()
            ref_data = response['data']
            for cited_paper in ref_data:
                cited_paper['citedPaper']['citedBy'] = paper_id
                ref_dict.append(cited_paper['citedPaper'])
        return ref_dict

@app.callback(
    Output('start-page', 'children'),
    Input('store-initial-query-response', 'data'))
def render_content(data):
    if data != None:
        return (html.Div([
            dcc.Tabs(id="tabs-example-graph", value = 'tab-1-example-graph', style = {'width': '306%', 'height': '10%', 'align-items':'center'},
                        children=[
                dcc.Tab(label='Search results', value='tab-1-example-graph',
                        style = {'order': '1', 'background-color': 'white', 'font-weight': 'bold'},
                        selected_style = {'order': '1', 'background-color': '#eda109', 'font-weight': 'bold'}),
                dcc.Tab(label='Reference landscape', value='tab-2-example-graph',
                        style = {'order': '2', 'background-color': 'white', 'font-weight': 'bold'},
                        selected_style = {'order': '2', 'background-color': '#eda109', 'font-weight': 'bold'}),
                dcc.Tab(label='Networks', value='tab-3-example-graph',
                        style = {'order': '3', 'background-color': 'white', 'font-weight': 'bold'},
                        selected_style = {'order': '3', 'background-color': '#eda109', 'font-weight': 'bold'})])],
                        style = {'backgroundColor': '#101126', 'width': '95%', 'height': '10%', 'display': 'flex',
                                    'flex-direction': 'row', 'margin' : 'auto', 'align-items': 'center'}),
        html.Br(),
        html.Br(),
        html.Div(id='tabs-content-example-graph'))
    else:
        return html.Div([html.H1("Welcome researcher!", style = {'color':'white', 'order':'1', 'margin':'auto', 'height':'20px'}),
                         html.P("You can start by entering keywords in the search bar above, or check the full documentation (upper right corner)",
                                style = {'color':'white', 'order':'2', 'margin':'auto', 'height':'20px'})],
                        style = {'width':'95%', 'height':'800px', 'margin':'auto', 'backgroundColor':'#101126',
                                 'display':'flex', 'flex-direction':'column', 'align-content':'center'})
    
@app.callback(Output('tabs-content-example-graph', 'children'),
              Input('tabs-example-graph', 'value'))
def render_tab_content(tab):
    if tab == 'tab-1-example-graph':
        return html.Div([
            html.Div([
        html.Div([
            html.H2("Earliest publication in", style={'color': '#eda109', 'font-family': 'Courier New, monospace'}),
            html.H1(id = 'earliest-pub-results', children=[], style={'color': 'white', 'font-family': 'Courier New, monospace'})],
            style={'width': '20%', 'height': '10%', 'order': '1', 'display': 'flex',
                   'flex-direction': 'column', 'align-items':'center', 'backgroundColor': '#101126'}),

        html.Div([
            html.H2("Latest publication in", style={'color': '#eda109', 'font-family': 'Courier New, monospace'}),
            html.H1(id = 'latest-pub-results', children = [], style={'color': 'white', 'font-family': 'Courier New, monospace'})],
            style={'width': '20%', 'height': '10%', 'order': '3', 'display': 'flex',
                   'flex-direction': 'column', 'align-items': 'center', 'backgroundColor': '#101126'}),

        html.Div([
            html.H2("Total results", style={'color': '#eda109', 'font-family': 'Courier New, monospace'}),
            html.H1(id = 'total-results', children = [], style = {'color': 'white', 'font-family': 'Courier New, monospace'})],
            style={'width': '30%', 'height': '10%', 'order': '2', 'display': 'flex',
                   'flex-direction': 'column', 'align-items': 'center', 'backgroundColor': '#101126'})
    ], style = {'backgroundColor':'#101126','width': '95%', 'display': 'flex', 'margin': 'auto',
                'flex-direction': 'row', 'align-items': 'center', 'justify-content': 'space-around'}),
    
    html.Br(),
    html.Br(),
    
    html.Div([
        html.Div([
            html.Div(id = 'keywords-graph-res', children= [], style = {'order': '1', 'backgroundColor': '#101126'}),
            html.Div(id = 'accessibility-pie-res', children = [], style = {'order': '2', 'backgroundColor': '#101126'})],
            style={'backgroundColor': '#101126', 'width': '95%', 'height':'30%', 'display': 'flex',
                    'flex-direction': 'row', 'align-items': 'center', 'margin' : 'auto',
                    'margin-top': '25px','justify-content': 'space-evenly'}),
        
        html.Br(),
        html.Br(),
        
        html.Div([
            html.Div(id = 'publication-graph-res', children = [], style = {'order': '1', 'backgroundColor': '#101126'}),
            html.Div(id = 'citations-graph-res', children = [], style = {'order': '2', 'backgroundColor': '#101126'})],
            style={'backgroundColor': '#101126', 'width': '95%', 'height':'30%', 'display': 'flex',
                'flex-direction': 'row', 'align-items': 'center', 'margin': 'auto',
                'margin-bottom': '25px', 'justify-content': 'space-evenly'}),
        
        html.Br(),
        html.Br(),
        
        html.Div([
            html.Div(id = 'fields-pie-res', children = [], style = {'order': '1', 'backgroundColor': '#101126'}),
            html.Div(id = 'active-authors-graph-res', children = [], style = {'order': '2', 'backgroundColor': '#101126'})],
            style={'backgroundColor': '#101126', 'width': '95%', 'height':'30%', 'display': 'flex',
                'flex-direction': 'row', 'align-items': 'center', 'margin': 'auto',
                'margin-bottom': '25px', 'justify-content': 'space-evenly'})
        ],
        
        style = {'backgroundColor': '#101126', 'width': '95%', 'display': 'flex',
                'flex-direction': 'column', 'align-items': 'center', 'margin': 'auto',
                'justify-content': 'space-evenly', 'margin-bottom': '20px'}),
    ])
    if tab == 'tab-2-example-graph':
        return html.Div([
            html.Div([
        html.Div([
            html.H2("Earliest publication in", style={'color': '#eda109', 'font-family': 'Courier New, monospace'}),
            html.H1(id = 'earliest-pub-ref', children = [], style={'color': 'white', 'font-family': 'Courier New, monospace'})],
            style={'width': '20%', 'height': '10%', 'order': '1', 'display': 'flex',
                   'flex-direction': 'column', 'align-items':'center', 'backgroundColor': '#101126'}),

        html.Div([
            html.H2("Latest publication in", style={'color': '#eda109', 'font-family': 'Courier New, monospace'}),
            html.H1(id = 'latest-pub-ref', children = [], style={'color': 'white', 'font-family': 'Courier New, monospace'})],
            style={'width': '20%', 'height': '10%', 'order': '3', 'display': 'flex',
                   'flex-direction': 'column', 'align-items': 'center', 'backgroundColor': '#101126'}),

        html.Div([
            html.H2("Total results", style={'color': '#eda109', 'font-family': 'Courier New, monospace'}),
            html.H1(id = 'total-results', children = [], style = {'color': 'white', 'font-family': 'Courier New, monospace'})],
            style={'width': '30%', 'height': '10%', 'order': '2', 'display': 'flex',
                   'flex-direction': 'column', 'align-items': 'center', 'backgroundColor': '#101126'})
    ], style = {'backgroundColor':'#101126','width': '95%', 'display': 'flex', 'margin': 'auto',
                'flex-direction': 'row', 'align-items': 'center', 'justify-content': 'space-around'}),
    
    html.Br(),
    html.Br(),
    
    html.Div([
        html.Div([
            html.Div(id = 'keywords-graph-ref', children= [], style = {'order': '1', 'backgroundColor': '#101126'}),
            html.Div(id = 'accessibility-pie-ref', children= [], style = {'order': '2', 'backgroundColor': '#101126'})],
            style={'backgroundColor': '#101126', 'width': '95%', 'display': 'flex',
                   'flex-direction': 'row', 'align-items': 'center', 'margin' : 'auto',
                   'margin-top': '25px','justify-content': 'space-evenly'}),
        
        html.Br(),
        html.Br(),
        
        html.Div([
            html.Div(id = 'publication-graph-ref', children= [], style = {'order': '1', 'backgroundColor': '#101126'}),
            html.Div(id = 'citations-graph-ref', children= [], style = {'order': '2', 'backgroundColor': '#101126'}),
        ], style={'backgroundColor': '#101126', 'width': '95%', 'display': 'flex',
                'flex-direction': 'row', 'align-items': 'center', 'margin': 'auto',
                'margin-bottom': '25px', 'justify-content': 'space-evenly'}),
        
        html.Br(),
        html.Br(),
        
        html.Div([
            html.Div(id = 'fields-pie-ref', children= [], style = {'order': '1', 'backgroundColor': '#101126'}),
            html.Div(id = 'active-authors-graph-ref', children= [], style = {'order': '2', 'backgroundColor': '#101126'})],
            style={'backgroundColor': '#101126', 'width': '95%', 'display': 'flex',
                   'flex-direction': 'row', 'align-items': 'center', 'margin': 'auto',
                   'margin-bottom': '25px', 'justify-content': 'space-evenly'})
        ],
        
        style = {'backgroundColor': '#101126', 'width': '95%', 'display': 'flex',
                'flex-direction': 'column', 'align-items': 'center', 'margin': 'auto',
                'justify-content': 'space-evenly', 'margin-bottom': '20px'}),
    ])
    if tab == 'tab-3-example-graph':
        return html.Div([
            
            html.Div([
                html.Div([
                    html.H2("Collaboration network", style = {'order':'1','font-size': '22px', 'font-family': 'Courier New, monospace',
                                                        'color': 'white'}),
                    cyto.Cytoscape(
                        id='cytoscape-event-callbacks-1',
                        layout={'name': 'circle', 'height': '600px', 'width': '600px'},
                        style = {'order': '2', 'height': '600px', 'width': '600px'},
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
                                    'line-color': 'lightgrey',
                                    'width': 0.7
                                }
                            }
                            ])],
                    
                style = {'order': '1', 'backgroundColor': '#101126', 'display': 'flex', 'flex-direction': 'column', 'align-items': 'center',
                        'width': '100%', 'height': '650px', 'margin-bottom': '20px', 'float': 'left'}),
        
                html.Br(),
                html.Br(),

                html.Div([
                    html.H2("Citation network", style = {'order': '1', 'font-size': '22px', 'font-family': 'Courier New, monospace',
                                                            'color': 'white'}),
                    cyto.Cytoscape(
                        id='cytoscape-event-callbacks-2',
                        layout={'name': 'cose', 'height': '900px', 'width': '750px'},
                        style={'order': '2', 'height': '900px', 'width': '750px'},
                        stylesheet = [
                            {
                                'selector': 'node',
                                'style': {
                                    'background-color': '#cb8deb',
                                    'height': '10px',
                                    'width': '10px'
                                } 
                            },
                            {
                                'selector': '.res',
                                'style': {
                                    'background-color': 'green',
                                    'color': 'red',
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
                                    'line-color': 'white',
                                    'width': 0.6
                                }
                            }
                            ])],
                    
                style = {'order': '2', 'width':'100%', 'height': '1000px', 'display': 'flex',
                        'flex-direction': 'column', 'align-items': 'center', 'backgroundColor': '#101126',
                        'margin-bottom': '20px'})],

                style = {'order': '1', 'width': '50%', 'height': '50%', 'display': 'flex', 'flex-direction': 'column', 'margin-left': '20px'}),
        
        html.Div([
                html.Div([
                    html.H2("Collaboration network", style = {'order':'1','font-size': '22px', 'font-family': 'Courier New, monospace',
                                                        'color': '#101126'}),
                    html.P("Click on a node to display information about an author",
                           style = {'order': '2', 'font-size': '22px',
                                    'font-family': 'Courier New, monospace', 'color': '#101126'}),
                    html.Div([
                        html.Img(src='/assets/user.png', style={'order': '1', 'height': '250px'}),
                        html.Div([
                            html.P(html.B("AUTHOR INFO"),
                                style = {'font-family': 'Courier New, monospace', 'color': '#101126', 'text-align': 'center'}),
                            html.Div(id = 'author-info-1', style = {'width': '95%', 'height': '95%', 'margin':'auto'})],
                        style = {'order': '2', 'width': '400px', 'height': '400px', 'border': "1px black solid"})],
                             style = {'order':'3', 'width':'95%', 'display': 'flex', 'flex-direction': 'row', 'align-items': 'center', 'margin-top': '50px', 'justify-content': 'space-around'}
                        )],
                    
                style = {'order': '1', 'backgroundColor': '#eda109', 'display': 'flex', 'flex-direction': 'column', 'align-items': 'center',
                        'width': '100%', 'height': '650px', 'margin-bottom': '20px', 'float': 'left'}),
        
                html.Br(),
                html.Br(),

                html.Div([
                    html.H2("Citation network", style = {'order': '1', 'font-size': '22px', 'font-family': 'Courier New, monospace',
                                                            'color': '#101126'}),
                    html.P("Click on a node to display information about a paper",
                           style = {'order': '2', 'font-size': '22px',
                                    'font-family': 'Courier New, monospace', 'color': '#101126'}),
                    html.Div([
                        html.Div([
                            html.P(html.B("PAPER INFO"),
                                   style = {'font-family': 'Courier New, monospace', 'color': '#101126', 'text-align': 'center'}),
                            html.Div(id = 'paper-info-1', style = {'width': '95%', 'height': '95%', 'margin':'auto'})],
                        style = {'order': '2', 'width': '95%', 'height': '840px', 'border': "1px black solid", "margin-top": "10px"})],
                                style = {'order':'3','width':'95%', 'display': 'flex', 'flex-direction': 'row', 'align-items': 'center', 'margin-top': '0px', 'justify-content': 'space-around'}
                        )],
                    
                style = {'order': '2', 'width':'100%', 'height': '1000px', 'display': 'flex',
                        'flex-direction': 'column', 'align-items': 'center', 'backgroundColor': '#eda109',
                        'margin-bottom': '20px'})],

                style = {'order': '2', 'width': '50%', 'height': '60%', 'display': 'flex', 'flex-direction': 'column', 'margin-right': '20px'})],
            
            style = {'display': 'flex', 'flex-direction': 'row', 'width': '97%', 'margin': 'auto', 'margin-bottom': '20px'})

# Topic title
@app.callback(
    Output('topic', 'children'),
    Input('search-query', 'value'))
def display_topic(value):
    if value != None:
        return f"Topic: {value}"
    else:
        return "Topic"

# Top flashacards -----------------------------------------------
@app.callback(
    Output('earliest-pub-results', 'children'),
    Input('store-initial-query-response', 'data'))
def create_earliest_pub_res(data):
    dff = pd.DataFrame(data['data'])
    return int(dff.year.min())

@app.callback(
    Output('earliest-pub-ref', 'children'),
    Input('store-references-query-response', 'data'))
def create_earliest_pub_ref(data):
    dff = pd.DataFrame(data)
    return int(dff.year.min())

@app.callback(
    Output('latest-pub-results', 'children'),
    Input('store-initial-query-response', 'data'))
def create_latest_pub_res(data):
    dff = pd.DataFrame(data['data'])
    return int(dff.year.max())

@app.callback(
    Output('latest-pub-ref', 'children'),
    Input('store-references-query-response', 'data'))
def create_latest_pub_ref(data):
    dff = pd.DataFrame(data)
    return int(dff.year.max())

@app.callback(
    Output('total-results', 'children'),
    Input('store-initial-query-response', 'data'))
def get_total_results(data):
    return int(data['total'])

# Plots and graphs ----------------------------------------------
# keywords
@app.callback(
    Output('keywords-graph-res', 'children'),
    Input('store-initial-query-response', 'data'))
def create_top_key_words_res(data):
    dff = pd.DataFrame(data['data'])
    dff = data_preprocess.extract_key_words(dff)
    fig = plots.make_top_key_words(dff)
    return dcc.Graph(figure=fig)

@app.callback(
    Output('keywords-graph-ref', 'children'),
    Input('store-references-query-response', 'data'))
def create_top_key_words_ref(data):
    dff = pd.DataFrame(data)
    dff = data_preprocess.extract_key_words(dff)
    fig = plots.make_top_key_words(dff)
    return dcc.Graph(figure=fig)

# accessibility
@app.callback(
    Output('accessibility-pie-res', 'children'),
    Input('store-initial-query-response', 'data'))
def create_accessibility_pie_res(data):
    dff = pd.DataFrame(data['data'])
    fig = plots.make_access_pie(dff)
    return dcc.Graph(figure=fig)

@app.callback(
    Output('accessibility-pie-ref', 'children'),
    Input('store-references-query-response', 'data'))
def create_accessibility_pie_ref(data):
    dff = pd.DataFrame(data)
    fig = plots.make_access_pie(dff)
    return dcc.Graph(figure=fig)

# publications per year
@app.callback(
    Output('publication-graph-res', 'children'),
    Input('store-initial-query-response', 'data'))
def create_publication_graph_res(data):
    dff = pd.DataFrame(data['data'])
    fig = plots.make_pub_per_year_line(dff)
    return dcc.Graph(figure=fig)

@app.callback(
    Output('publication-graph-ref', 'children'),
    Input('store-references-query-response', 'data'))
def create_publication_graph_ref(data):
    dff = pd.DataFrame(data)
    fig = plots.make_pub_per_year_line(dff)
    return dcc.Graph(figure=fig)

# citations per year
@app.callback(
    Output('citations-graph-res', 'children'),
    Input('store-initial-query-response', 'data'))
def create_citations_graph_res(data):
    dff = pd.DataFrame(data['data'])
    fig = plots.make_citations_per_year_line(dff)
    return dcc.Graph(figure=fig)

@app.callback(
    Output('citations-graph-ref', 'children'),
    Input('store-references-query-response', 'data'))
def create_citations_graph_ref(data):
    dff = pd.DataFrame(data)
    fig = plots.make_citations_per_year_line(dff)
    return dcc.Graph(figure=fig)

# fields of study
@app.callback(
    Output('fields-pie-res', 'children'),
    Input('store-initial-query-response', 'data'))
def create_fields_pie_res(data):
    dff = pd.DataFrame(data['data'])
    fig = plots.make_fields_pie(dff)
    return dcc.Graph(figure=fig)

@app.callback(
    Output('fields-pie-ref', 'children'),
    Input('store-references-query-response', 'data'))
def create_citations_graph_ref(data):
    dff = pd.DataFrame(data)
    fig = plots.make_fields_pie(dff)
    return dcc.Graph(figure=fig)

# most active authors
@app.callback(
    Output('active-authors-graph-res', 'children'),
    Input('store-initial-query-response', 'data'))
def create_active_authors_graph_res(data):
    dff = pd.DataFrame(data['data'])
    fig = plots.make_active_authors(dff)
    return dcc.Graph(figure=fig)

@app.callback(
    Output('active-authors-graph-ref', 'children'),
    Input('store-references-query-response', 'data'))
def create_citations_graph_ref_ref(data):
    dff = pd.DataFrame(data)
    fig = plots.make_active_authors(dff)
    return dcc.Graph(figure=fig)

# Cytoscapes -------------------------------------------------------------------
@app.callback(
    Output('cytoscape-event-callbacks-1', 'elements'),
    Input('store-initial-query-response', 'data'))
def generate_collaboration_network(data):
    dff = pd.DataFrame(data['data'])
    elements = plots.generate_graph_elements_collab(dff)
    return elements

@app.callback(
    Output('cytoscape-event-callbacks-2', 'elements'),
    Input('store-references-query-response', 'data'),
    Input('store-initial-query-response', 'data'))
def generate_collaboration_network(data_ref, data_res):
    ref_df = pd.DataFrame(data_ref)
    ref_df['reference'] = semantic_api.build_references(ref_df)
    res_df = pd.DataFrame(data_res['data'])
    res_df['reference'] = semantic_api.build_references(res_df)
    elements= plots.generate_graph_elements_network(ref_df, res_df)
    return elements
              
@app.callback(Output('author-info-1', 'children'),
              Input('cytoscape-event-callbacks-1', 'tapNodeData'))
def displayTapNodeData(data):
    if data:
        author_info = semantic_api.get_author_info(data['id'])
        paragraph = html.P([html.Br(), html.U("Author Id"), f": {author_info['authorId']}", html.Br(),html.Br(),
                            html.U("Name"), f": {author_info['name']}", html.Br(),html.Br(),
                            html.U("Affiliation(s)"), f": {author_info['affiliations']}", html.Br(),html.Br(),
                            html.U("Homepage"), f": {author_info['homepage']}", html.Br(),html.Br(),
                            html.U("Paper count"), f": {author_info['paperCount']}", html.Br(),html.Br(),
                            html.U("Citation count"), f": {author_info['citationCount']}", html.Br(),html.Br(),
                            html.U(f"h index"), f": {author_info['hIndex']}", html.Br(), html.Br(),
                            html.A('Semantic Scholar URL', href = author_info['url'], target = '_blank'), html.Br(), html.Br(),],
                            style = {'text-align': 'left', 'color': '#101126'})
        return paragraph

@app.callback(Output('paper-info-1', 'children'),
              Input('cytoscape-event-callbacks-2', 'tapNodeData'))
def displayTapNodeData(data):
    if data:
        paper_info = semantic_api.get_paper_info(data['id'])
        if 'paperId' in paper_info:
            paragraph = html.P([html.Br(), html.U("Title"), f": {paper_info['title']}", html.Br(),html.Br(),
                                html.U("Venue"), f": {paper_info['venue']}", html.Br(),html.Br(),
                                html.U("Year"), f": {paper_info['year']}", html.Br(),html.Br(),
                                html.U("Ref. count"), f": {paper_info['referenceCount']}", html.Br(),html.Br(),
                                html.U("Citation count"), f": {paper_info['citationCount']}", html.Br(),html.Br(),
                                html.U(f"Open Access"), f": {paper_info['isOpenAccess']}", html.Br(), html.Br(),
                                html.A('Semantic Scholar URL', href = paper_info['url'], target = '_blank'), html.Br(), html.Br(),
                                html.U("Abstract"), f": {paper_info['abstract']}"],
                                style = {'text-align': 'left', 'color': '#101126'})
        else:
            paragraph = html.P("No info available for this paper")
        return paragraph

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)