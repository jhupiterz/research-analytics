#--------------------------------------------------------------------------#
#                   This code makes use of all other functions of          #
#                      the package to build a Dash Web App                 # 
#--------------------------------------------------------------------------#

# imports ------------------------------------------------------------------
from cmath import nan
import plots
import utils
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
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1", 'charSet':'“UTF-8”'}])


app.title = "Research Intelligence"

# Layout --------------------------------------------------------------------
app.layout = html.Div(
    [
        # Banner ------------------------------------------------------------
        html.Div(
            [
                html.A(
                    [
                        html.Img(
                            src="/assets/brain.png",
                            alt="research intelligence",
                        ),
                        html.H3("research analytics"),
                    ],
                    href="https://jhupiterz.notion.site/Welcome-to-research-intelligence-a36796f418b040f6ade944f9c54e87cb",
                    target='_blank',
                    className="logo-banner",
                ),
                html.Div(
                    [
                        html.A(
                            "Contribute", 
                            href="https://github.com/jhupiterz/research-analytics",
                            target='_blank', 
                            className="doc-link"
                        ),
                        html.A(
                            "Documentation", 
                            href="https://github.com/jhupiterz/research-analytics/blob/main/README.md",
                            target='_blank', 
                            className="doc-link"
                        ),
                    
                    ],
                    className="navbar"
                ),
            ],
            className="banner",
        ),
        
        html.Div(
            [
                html.H1(id='topic', children=[]),
                html.Div(
                    [
                        html.Img(
                            src='/assets/loupe.png', 
                            className="loupe-img",
                        ),
                        dcc.Input(
                            id='search-query',
                            type = 'text',
                            placeholder = "Search for keywords (e.g. \"carbon nanotubes\")",
                            debounce = True,
                            spellCheck = True,
                            inputMode = 'latin',
                            name = 'text',
                            autoFocus = False,
                            minLength = 1, maxLength = 60,
                            autoComplete='off',
                            disabled = False,
                            readOnly = False,
                            size = '60',
                            n_submit = 0,
                        ),
                    ], 
                    className="search-bar",
                ),
            ],
            className="search-wrapper"
        ),
        
        dcc.Store(id='store-initial-query-response', storage_type='memory'),
        dcc.Store(id='store-references-query-response', storage_type='memory'),
        
        html.Div(id='start-page', children=[]),
        
        # Footer -----------------------------------------------------------
        html.Footer(
            [
                html.P(
                    [
                        "Built with ", 
                        html.A("Plotly Dash", href="https://plotly.com/dash/", target="_blank")
                    ],
                ),
                html.P(
                    [
                        "Powered by ", 
                        html.A("Semantic Scholar", href="https://www.semanticscholar.org/", target="_blank")
                    ],
                ),
            ]
        ),
    ],
    className="app-layout",
)

# Callbacks --------------------------------------------------------------------
# Store response of initial API query
@app.callback(
    Output('store-initial-query-response', 'data'),
    Input('search-query', 'n_submit'),
    Input('search-query', 'value'))
def store_primary_data(n_submit, value):
    if n_submit > 0:
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
            dcc.Tabs(id="tabs-example-graph", value = 'tab-1-example-graph', style = {'height': '6vh', 'width': '94vw', 'text-align':'center','display':'flex', 'flex-direction':'row'},
                        children=[
                dcc.Tab(label='📊 Search results 📊', value='tab-1-example-graph',
                        style = {'order': '1', 'background-color': 'white', 'font-weight': 'bold', 'text-align':'center', 'font-family':'Arial, sans serif', 'color':'black', 'border': '1px', 'border-radius': '5px', 'margin-left': '15px'},
                        selected_style = {'order': '1', 'background-color': '#eda109', 'font-weight': 'bold', 'text-align':'center', 'font-family':'Arial, sans serif', 'border': '1px', 'border-radius': '5px', 'border-color':'white', 'margin-left': '15px'}),
                dcc.Tab(label='🥷 Author network 🥷', value='tab-2-example-graph',
                        style = {'order': '2', 'background-color': 'white', 'font-weight': 'bold', 'text-align':'center', 'font-family':'Arial, sans serif', 'color':'black', 'border': '1px', 'border-radius': '5px', 'margin-left': '15px'},
                        selected_style = {'order': '2', 'background-color': '#eda109', 'font-weight': 'bold', 'text-align':'center', 'font-family':'Arial, sans serif', 'border': '1px', 'border-radius': '5px', 'border-color':'white', 'margin-left': '15px'}),
                dcc.Tab(label='📚 Paper network 📚', value='tab-3-example-graph',
                        style = {'order': '3', 'background-color': 'white', 'font-weight': 'bold', 'text-align':'center', 'font-family':'Arial, sans serif', 'color':'black', 'border': '1px', 'border-radius': '5px', 'margin-left': '15px'},
                        selected_style = {'order': '3', 'background-color': '#eda109', 'font-weight': 'bold', 'text-align':'center', 'font-family':'Arial, sans serif', 'border': '1px', 'border-radius': '5px', 'border-color':'white', 'margin-left': '15px'})])],
                        style = {'width': '95%', 'height': '6vh', 'display': 'flex',
                                    'flex-direction': 'row', 'margin' : 'auto', 'align-items': 'center', 'text-align':'center'}),
        html.Br(),
        html.Div(id='tabs-content-example-graph'))
    else:
        return html.Div(
            [
                html.Hr(style={'order':'1', 'width': '60%', 'margin-top': '-6vh'}),
                html.P("Or start with one of our example dashboards", style={'order':'2', 'text-align': 'center', 'font-size':'2.5vh'})
            ],
            style={'min-height':'300px', 'display':'flex', 'flex-direction':'column', 'text-align':'center'}
        )
    
@app.callback(Output('tabs-content-example-graph', 'children'),
              Input('tabs-example-graph', 'value'))
def render_tab_content(tab):
    if tab == 'tab-1-example-graph':
        return html.Div([
        html.Div([
            dcc.Loading(id = "loading-icon-1",
                children=[html.Div(id = 'keywords-graph-all', children= [], style = {'order': '1', 'backgroundColor': '#101126'})], type = 'default'),
            html.Div(id = 'accessibility-pie-all', children = [html.Div(id = 'dp-access', children=[], style = {'order': '2', 'margin-left': '-2vw'}),
                                                               html.Div(id = 'access-pie-all', children= [], style = {'order': '1', 'backgroundColor': '#101126',
                                                                                                                      'display':'flex', 'flex-direction':'row',
                                                                                                                      'align-items':'center', 'margin-right': '-2vw'})],
                     style = {'order': '2', 'display': 'flex', 'flex-direction': 'row', 'align-items': 'center'})],
            style={'backgroundColor': '#101126', 'width': '95%', 'height':'30%', 'display': 'flex',
                    'flex-direction': 'row', 'align-items': 'center', 'margin' : 'auto',
                    'margin-top': '3vh','justify-content': 'space-evenly'}),
        
        html.Br(),
        html.Br(),
        
        html.Div([
            html.Div(id = 'publication-graph-all', children = [], style = {'order': '1', 'backgroundColor': '#101126'}),
            html.Div(id = 'citations-graph-all', children = [], style = {'order': '2', 'backgroundColor': '#101126'})],
            style={'backgroundColor': '#101126', 'width': '95%', 'height':'30%', 'display': 'flex',
                'flex-direction': 'row', 'align-items': 'center', 'margin': 'auto',
                'margin-bottom': '3vh', 'justify-content': 'space-evenly'}),
        
        html.Br(),
        html.Br(),
        
        html.Div([
            html.Div(id = 'fields-pie-all', children = [], style = {'order': '1', 'backgroundColor': '#101126'}),
            html.Div(id = 'active-authors-graph-all', children = [], style = {'order': '2', 'backgroundColor': '#101126'})],
            style={'backgroundColor': '#101126', 'width': '95%', 'height':'30%', 'display': 'flex',
                'flex-direction': 'row', 'align-items': 'center', 'margin': 'auto',
                'margin-bottom': '3vh', 'justify-content': 'space-evenly'})
        ],
        
        style = {'backgroundColor': '#101126', 'width': '94vw', 'display': 'flex',
                'flex-direction': 'column', 'align-items': 'center', 'margin': 'auto',
                'justify-content': 'space-evenly', 'border-radius': '20px', 'margin-bottom': '3vh'})
    
    if tab == 'tab-2-example-graph':
        return html.Div([
            html.Div([
                    html.H2("Collaboration network", style = {'order':'1','font-size': '2.5vh', 'font-family': 'Courier New, monospace',
                                                        'color': 'white'}),
                    html.Button('Reset view', id='bt-reset', className= 'reset-button'),
                    html.Div(id = 'dp-access', ),
                    cyto.Cytoscape(
                        id='cytoscape-event-callbacks-1',
                        layout={'name': 'circle', 'height': '55vh', 'width': '38vw'},
                        style = {'order': '3', 'height': '55vh', 'width': '38vw'},
                        stylesheet = [
                            {
                                'selector': 'label',
                                'style': {
                                    'content': 'data(label)',
                                    'color': 'white',
                                    'font-size':'14vh',
                                    'font-family':'Arial, sans serif',
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
                    
                style = {'order': '1', 'backgroundColor': '#101126', 'display': 'flex', 'flex-direction': 'column',
                         'align-items': 'center', 'width': '45%', 'height': '65vh', 'margin-bottom': '3vh', 'float': 'left', 'border-radius': '20px'}),
            
            html.Div([
                    html.H2("Collaboration network", style = {'order':'1','font-size': '2.5vh', 'font-family': 'Courier New, monospace',
                                                        'color': '#101126'}),
                    html.P("Click on a node to display information about an author",
                           style = {'order': '2', 'font-size': '2vh', 'text-align':'center',
                                    'font-family': 'Courier New, monospace', 'color': '#101126'}),
                    html.Div([
                        html.Img(src='/assets/user.png', style={'order': '1', 'height': '30vh'}),
                        html.Div([
                            html.P(html.B("AUTHOR INFO"),
                                style = {'font-family': 'Courier New, monospace', 'color': '#101126', 'text-align': 'center'}),
                            html.Div(id = 'author-info-1', style = {'width': '95%', 'height': '80%', 'margin':'auto'})],
                        style = {'order': '2', 'width': '35vh', 'height': '40vh', 'border': "0.2vh black solid", 'overflow-y':'auto', 'border-radius': '5px'})],
                             style = {'order':'3', 'width':'95%', 'display': 'flex', 'flex-direction': 'row', 'align-items': 'center', 'margin-top': '4vh', 'justify-content': 'space-around'}
                        )],
                    
                style = {'order': '2', 'backgroundColor': '#eda109', 'display': 'flex', 'flex-direction': 'column', 'align-items': 'center',
                        'width': '45%', 'height': '65vh', 'float': 'left', 'border-radius': '20px', 'margin-bottom': '3vh'})
    
    ], style={'display': 'flex', 'flex-direction': 'row', 'align-items':'center',
              'justify-content':'space-between', 'min-height':'75vh', 'width': '94vw',
              'margin': 'auto', 'border-radius': '20px'})
        
    if tab == 'tab-3-example-graph':
        return html.Div([

                html.Div([
                    html.H2("Citation network", style = {'order': '1', 'font-size': '2.5vh', 'font-family': 'Courier New, monospace',
                                                         'color': 'white'}),
                    
                    html.Button('Reset view', id='bt-reset-papers', className= 'reset-button'),
                    cyto.Cytoscape(
                        id='cytoscape-event-callbacks-2',
                        layout={'name': 'cose', 'height': '85vh', 'width': '70vh'},
                        style={'order': '2', 'height': '85vh', 'width': '70vh'},
                        stylesheet = [
                            {
                                'selector': 'node',
                                'style': {
                                    'background-color': '#cb8deb',
                                    'height': '8vh',
                                    'width': '8vh'
                                } 
                            },
                            {
                                'selector': '.res',
                                'style': {
                                    'background-color': 'green',
                                    'color': 'red',
                                    'height': '1.2vh',
                                    'width': '1.2vh'
                                }
                            },
                            {
                                'selector': '.ref',
                                'style': {
                                    'background-color': 'white',
                                    'color': 'white',
                                    'height': '0.8vh',
                                    'width': '0.8vh'
                                }
                            },
                            {
                                'selector': '.citation',
                                'style': {
                                    'line-color': 'white',
                                    'width': '0.4vh'
                                }
                            }
                            ])],
                    
                style = {'order': '1', 'width':'45%', 'height': '65vh', 'display': 'flex',
                        'flex-direction': 'column', 'align-items': 'center', 'backgroundColor': '#101126',
                        'margin-bottom': '3vh', 'border-radius': '20px'}),


                html.Div([
                    html.H2("Citation network", style = {'order': '1', 'font-size': '2.5vh', 'font-family': 'Courier New, monospace',
                                                            'color': '#101126'}),
                    html.P("Click on a node to display information about a paper",
                           style = {'order': '2', 'font-size': '2vh', 'text-align':'center',
                                    'font-family': 'Courier New, monospace', 'color': '#101126'}),
                    html.Div([
                        html.Div([
                            html.P(html.B("PAPER INFO"),
                                   style = {'font-family': 'Courier New, monospace', 'color': '#101126', 'text-align': 'center'}),
                            html.Div(id = 'paper-info-1', style = {'width': '95%', 'height': '90%', 'margin':'auto'})],
                        style = {'order': '2', 'width': '95%', 'height': '45vh', 'border': "0.2vh black solid", "margin-top": "1.5vh", 'overflow-y':'auto', 'border-radius': '5px'})],
                                style = {'order':'3','width':'95%', 'display': 'flex', 'flex-direction': 'row', 'align-items': 'center', 'margin-top': '0vh', 'justify-content': 'space-around'}
                        )],
                    
                style = {'order': '2', 'width':'45%', 'height': '65vh', 'display': 'flex',
                        'flex-direction': 'column', 'align-items': 'center', 'backgroundColor': '#eda109',
                        'margin-bottom': '3vh', 'border-radius': '20px'})],
            
            style = {'display': 'flex', 'flex-direction': 'row', 'align-items':'center',
                     'justify-content':'space-between', 'min-height':'75vh', 'width': '94vw',
                     'margin': 'auto', 'border-radius': '20px'})

# Topic title
@app.callback(
    Output('topic', 'children'),
    Input('search-query', 'value'))
def display_topic(value):
    if value != None:
        return f"Topic: {value}"
    else:
        return "Welcome researcher! 🧠"

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
    Input('store-initial-query-response', 'data'),
    Input('search-query', 'value'))
def create_top_key_words_res(data, query):
    dff = pd.DataFrame(data['data'])
    dff = data_preprocess.extract_key_words(dff)
    fig = plots.make_top_key_words(dff, query)
    return dcc.Graph(figure=fig, style = {'width':'40vw', 'height':'45vh'})

@app.callback(
    Output('keywords-graph-ref', 'children'),
    Input('store-references-query-response', 'data'),
    Input('search-query', 'value'))
def create_top_key_words_ref(data, query):
    dff = pd.DataFrame(data)
    dff = data_preprocess.extract_key_words(dff)
    fig = plots.make_top_key_words(dff, query)
    return dcc.Graph(figure=fig, style = {'width':'40vw', 'height':'45vh'})

@app.callback(
    Output('keywords-graph-all', 'children'),
    Input('store-initial-query-response', 'data'),
    Input('store-references-query-response', 'data'),
    Input('search-query', 'value'))
def create_top_key_words_all(data_res, data_ref, query):
    dff_res = pd.DataFrame(data_res['data'])
    dff_res['result'] = 'direct'
    dff_res = data_preprocess.extract_key_words(dff_res)
    dff_ref = pd.DataFrame(data_ref)
    dff_ref['result'] = 'reference'
    dff_ref = data_preprocess.extract_key_words(dff_ref)
    dff_all = pd.concat([dff_res, dff_ref])
    fig = plots.make_top_key_words(dff_all, query)
    return dcc.Graph(figure=fig, style = {'width':'40vw', 'height':'45vh'})

# loading states for keyword graphs
@app.callback(Output('loading-icon-1', 'children'),
              Input('keywords-graph-res', 'children'))

@app.callback(Output('loading-icon-2', 'children'),
              Input('keywords-graph-ref', 'children'))

# accessibility
@app.callback(
    Output('accessibility-pie-res', 'children'),
    Input('store-initial-query-response', 'data'))
def create_accessibility_pie_res(data):
    dff = pd.DataFrame(data['data'])
    fig = plots.make_access_pie(dff)
    return dcc.Graph(figure=fig, style = {'width':'40vw', 'height':'45vh'})

@app.callback(
    Output('accessibility-pie-ref', 'children'),
    Input('store-references-query-response', 'data'))
def create_accessibility_pie_ref(data):
    dff = pd.DataFrame(data)
    fig = plots.make_access_pie(dff)
    return dcc.Graph(figure=fig, style = {'width':'40vw', 'height':'45vh'})

# Generate the dropdown menu according to all fields of study in data
@app.callback(
    Output('dp-access', 'children'),
    Input('store-initial-query-response', 'data'),
    Input('store-references-query-response', 'data'))
def create_accessibility_pie_all(data_res, data_ref):
    dff_res = pd.DataFrame(data_res)
    dff_res['result'] = 'direct'
    dff_ref = pd.DataFrame(data_ref)
    dff_ref['result'] = 'reference'
    dff_all = pd.concat([dff_res, dff_ref])
    fields_of_study = dff_all['fieldsOfStudy'].tolist()
    res = [field for field in fields_of_study if isinstance(field, list)]
    flat_list_fields = utils.flatten_list(res)
    options = ['All'] + list(set(flat_list_fields))
    return dcc.Dropdown(id = 'dp-access-component', value = 'All', options = options, clearable=False, placeholder= 'Select a field of study', className= 'dp-access-pie', style={'order':'2'})


@app.callback(
    Output('access-pie-all', 'children'),
    Input('store-initial-query-response', 'data'),
    Input('store-references-query-response', 'data'),
    Input('dp-access-component', 'value'))
def create_accessibility_pie_all(data_res, data_ref, filter):
    dff_res = pd.DataFrame(data_res)
    dff_res['result'] = 'direct'
    dff_ref = pd.DataFrame(data_ref)
    dff_ref['result'] = 'reference'
    dff_all = pd.concat([dff_res, dff_ref])
    if filter == 'All':
        fig = plots.make_access_pie(dff_all)
    else:
        index_list = []
        for index, row in dff_all.iterrows():
            if isinstance(row.fieldsOfStudy, list):
                if filter in row.fieldsOfStudy:
                    index_list.append(index)
        dff_filtered = dff_all.loc[index_list]
        fig = plots.make_access_pie(dff_filtered)
    return dcc.Graph(className = 'access-pie', figure = fig, style={'order':'1'})

# publications per year
@app.callback(
    Output('publication-graph-res', 'children'),
    Input('store-initial-query-response', 'data'))
def create_publication_graph_res(data):
    dff = pd.DataFrame(data['data'])
    fig = plots.make_pub_per_year_line(dff)
    return dcc.Graph(figure=fig, style = {'width':'40vw', 'height':'45vh'})

@app.callback(
    Output('publication-graph-ref', 'children'),
    Input('store-references-query-response', 'data'))
def create_publication_graph_ref(data):
    dff = pd.DataFrame(data)
    fig = plots.make_pub_per_year_line(dff)
    return dcc.Graph(figure=fig, style = {'width':'40vw', 'height':'45vh'})

@app.callback(
    Output('publication-graph-all', 'children'),
    Input('store-initial-query-response', 'data'),
    Input('store-references-query-response', 'data'))
def create_publication_graph_all(data_res, data_ref):
    dff_res = pd.DataFrame(data_res['data'])
    dff_res['result'] = 'direct'
    dff_ref = pd.DataFrame(data_ref)
    dff_ref['result'] = 'reference'
    dff_all = pd.concat([dff_res, dff_ref])
    fig = plots.make_pub_per_year_line(dff_all)
    return dcc.Graph(figure=fig, style = {'width':'40vw', 'height':'45vh'})

# citations per year
@app.callback(
    Output('citations-graph-res', 'children'),
    Input('store-initial-query-response', 'data'))
def create_citations_graph_res(data):
    dff = pd.DataFrame(data['data'])
    fig = plots.make_citations_per_year_line(dff)
    return dcc.Graph(figure=fig, style = {'width':'40vw', 'height':'45vh'})

@app.callback(
    Output('citations-graph-all', 'children'),
    Input('store-initial-query-response', 'data'),
    Input('store-references-query-response', 'data'))
def create_citations_graph_all(data_res, data_ref):
    dff_res = pd.DataFrame(data_res['data'])
    dff_res['result'] = 'direct'
    dff_ref = pd.DataFrame(data_ref)
    dff_ref['result'] = 'reference'
    dff_all = pd.concat([dff_res, dff_ref])
    fig = plots.make_citations_per_year_line(dff_all)
    return dcc.Graph(figure=fig, style = {'width':'40vw', 'height':'45vh'})

@app.callback(
    Output('citations-graph-ref', 'children'),
    Input('store-references-query-response', 'data'))
def create_citations_graph_ref(data):
    dff = pd.DataFrame(data)
    fig = plots.make_citations_per_year_line(dff)
    return dcc.Graph(figure=fig, style = {'width':'40vw', 'height':'45vh'})

# fields of study
@app.callback(
    Output('fields-pie-res', 'children'),
    Input('store-initial-query-response', 'data'))
def create_fields_pie_res(data):
    dff = pd.DataFrame(data['data'])
    fig = plots.make_fields_pie(dff)
    return dcc.Graph(figure=fig, style = {'width':'40vw', 'height':'45vh'})

@app.callback(
    Output('fields-pie-ref', 'children'),
    Input('store-references-query-response', 'data'))
def create_citations_graph_ref(data):
    dff = pd.DataFrame(data)
    fig = plots.make_fields_pie(dff)
    return dcc.Graph(figure=fig, style = {'width':'40vw', 'height':'45vh'})

@app.callback(
    Output('fields-pie-all', 'children'),
    Input('store-initial-query-response', 'data'),
    Input('store-references-query-response', 'data'))
def create_fields_pie_res(data_res, data_ref):
    dff_res = pd.DataFrame(data_res['data'])
    dff_res['result'] = 'direct'
    dff_ref = pd.DataFrame(data_ref)
    dff_ref['result'] = 'reference'
    dff_all = pd.concat([dff_res, dff_ref])
    fig = plots.make_fields_pie(dff_all)
    return dcc.Graph(figure=fig, style = {'width':'40vw', 'height':'45vh'})

# most active authors
@app.callback(
    Output('active-authors-graph-res', 'children'),
    Input('store-initial-query-response', 'data'))
def create_active_authors_graph_res(data):
    dff = pd.DataFrame(data['data'])
    fig = plots.make_active_authors(dff)
    return dcc.Graph(figure=fig, style = {'width':'40vw', 'height':'45vh'})

@app.callback(
    Output('active-authors-graph-ref', 'children'),
    Input('store-references-query-response', 'data'))
def create_citations_graph_ref_ref(data):
    dff = pd.DataFrame(data)
    fig = plots.make_active_authors(dff)
    return dcc.Graph(figure=fig, style = {'width':'40vw', 'height':'45vh'})

@app.callback(
    Output('active-authors-graph-all', 'children'),
    Input('store-initial-query-response', 'data'),
    Input('store-references-query-response', 'data'))
def create_active_authors_graph_res(data_res, data_ref):
    dff_res = pd.DataFrame(data_res['data'])
    dff_res['result'] = 'direct'
    dff_ref = pd.DataFrame(data_ref)
    dff_ref['result'] = 'reference'
    dff_all = pd.concat([dff_res, dff_ref])
    fig = plots.make_active_authors(dff_all)
    return dcc.Graph(figure=fig, style = {'width':'40vw', 'height':'45vh'})

# Cytoscapes -------------------------------------------------------------------
@app.callback(
    Output('cytoscape-event-callbacks-1', 'elements'),
    Output('cytoscape-event-callbacks-1', 'zoom'),
    Input('store-initial-query-response', 'data'),
    Input('bt-reset', 'n_clicks'),
    Input('cytoscape-event-callbacks-1', 'zoom'))
def generate_collaboration_network(data_res, n_clicks, zoom):
    dff_res = pd.DataFrame(data_res['data'])
    dff_res['result'] = 'direct'
    elements = plots.generate_graph_elements_collab(dff_res)
    if n_clicks:
        if n_clicks > 0:
            zoom = 1
            return elements, zoom
    return elements, zoom

@app.callback(
    Output('cytoscape-event-callbacks-2', 'elements'),
    Output('cytoscape-event-callbacks-2', 'zoom'),
    Input('store-references-query-response', 'data'),
    Input('store-initial-query-response', 'data'),
    Input('bt-reset-papers', 'n_clicks'),
    Input('cytoscape-event-callbacks-2', 'zoom'))
def generate_citation_network(data_ref, data_res, n_clicks, zoom):
    ref_df = pd.DataFrame(data_ref)
    ref_df['reference'] = semantic_api.build_references(ref_df)
    res_df = pd.DataFrame(data_res['data'])
    res_df['reference'] = semantic_api.build_references(res_df)
    elements= plots.generate_graph_elements_network(ref_df, res_df)
    if n_clicks:
        if n_clicks > 0:
            zoom = 1
            return elements, zoom
    return elements, zoom
              
# Retrieves info on author
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

# Retrieves info on paper
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