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
import plotly.express as px
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
                            src="/assets/web.png",
                            alt="research intelligence", style = {'width': '10vw', 'margin-left': '-3vw'}
                        ),
                        html.H3("research analytics", style= {'margin-left': '-3vw'}),
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
                html.H1(id='topic', children=[], style = {'color': '#13070C'}),
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
            dcc.Tabs(id="tabs-example-graph", value = 'tab-1-example-graph', style = {'height': '6vh', 'width': '85vw', 'text-align':'center','display':'flex', 'flex-direction':'row', 'margin': 'auto'},
                        children=[
                dcc.Tab(label='📊  Search results  📊', value='tab-1-example-graph',
                        style = {'order': '1', 'background-color': 'white', 'font-weight': 'bold', 'text-align':'center', 'font-family':'Arial, sans serif', 'color':'black', 'border': '1px', 'border-radius': '5px', 'box-shadow': '0px 0px 15px rgba(0, 0, 0, 0.2)', 'margin-right': '2vw'},
                        selected_style = {'order': '1', 'background-color': px.colors.sequential.Plotly3[9], 'font-weight': 'bold', 'text-align':'center', 'font-family':'Arial, sans serif', 'border': '1px', 'border-radius': '5px', 'border-color':'white', 'box-shadow': '0px 0px 15px rgba(0, 0, 0, 0.2)', 'margin-right': '2vw'}),
                dcc.Tab(label='🤝  Author network  🤝', value='tab-2-example-graph',
                        style = {'order': '2', 'background-color': 'white', 'font-weight': 'bold', 'text-align':'center', 'font-family':'Arial, sans serif', 'color':'black', 'border': '1px', 'border-radius': '5px', 'margin': 'auto', 'box-shadow': '0px 0px 15px rgba(0, 0, 0, 0.2)'},
                        selected_style = {'order': '2', 'background-color': px.colors.sequential.Plotly3[9], 'font-weight': 'bold', 'text-align':'center', 'font-family':'Arial, sans serif', 'border': '1px', 'border-radius': '5px', 'border-color':'white', 'margin': 'auto', 'box-shadow': '0px 0px 15px rgba(0, 0, 0, 0.2)'}),
                dcc.Tab(label='🌐  Paper network  🌐', value='tab-3-example-graph',
                        style = {'order': '3', 'background-color': 'white', 'font-weight': 'bold', 'text-align':'center', 'font-family':'Arial, sans serif', 'color':'black', 'border': '1px', 'border-radius': '5px', 'box-shadow': '0px 0px 15px rgba(0, 0, 0, 0.2)', 'margin-left': '2vw'},
                        selected_style = {'order': '3', 'background-color': px.colors.sequential.Plotly3[9], 'font-weight': 'bold', 'text-align':'center', 'font-family':'Arial, sans serif', 'border': '1px', 'border-radius': '5px', 'border-color':'white', 'box-shadow': '0px 0px 15px rgba(0, 0, 0, 0.2)', 'margin-left': '2vw'})])],
                        style = {'width': '85vw', 'height': '6vh', 'display': 'flex', 'margin-left':'8vw',
                                 'flex-direction': 'row', 'margin' : 'auto', 'align-items': 'center', 'text-align':'center'}),
        html.Br(),
        html.Div(id='tabs-content-example-graph'))
    else:
        return html.Div(
            [
                html.Hr(style={'order':'1', 'width': '60%', 'margin-top': '-14vh'}),
                html.P("Check out the latest blog posts about data in academia", style={'order':'2', 'text-align': 'center', 'font-size':'2.5vh', 'color': '#13070C'}), html.Br(),
                html.Div([
                html.A(
                        href="https://medium.com/@juhartz/are-scholarly-papers-really-the-best-way-to-disseminate-research-f8d85d3eee62",
                        children=[
                            html.Img(
                                alt="Link to my twitter",
                                src="assets/blogpost_1.png",
                                className="zoom"
                            )
                        ], target= '_blank', style = {'order': '1', 'margin-top': '5vh', 'margin-bottom': '-5vh'}
                    ),
                html.A(
                        href="https://medium.com/@juhartz/what-makes-a-research-paper-impactful-a40f33206fd1",
                        children=[
                            html.Img(
                                alt="Link to my twitter",
                                src="assets/blogpost_2.png",
                                className='zoom'
                            )
                        ], target= '_blank', style = {'order': '2', 'margin-top': '5vh', 'margin-left': '5vw', 'margin-bottom': '-5vh'}
                    )
            ],
            style={'order':'3', 'display':'flex', 'flex-direction':'row', 'text-align':'center', 'margin': 'auto'})],
            style = {'min-height':'300px', 'display':'flex', 'flex-direction':'column', 'text-align':'center'})
    
@app.callback(Output('tabs-content-example-graph', 'children'),
              Input('tabs-example-graph', 'value'))
def render_tab_content(tab):
    if tab == 'tab-1-example-graph':
        return html.Div([
        html.Div([
            dcc.Loading(id = "loading-icon-1",
                children=[html.Div(id = 'keywords-graph-all', children= [], style = {'order': '1', 'backgroundColor': 'white', 'border-radius':'5px', 'box-shadow': '0px 0px 15px rgba(0, 0, 0, 0.2)'})], type = 'default'),
            
            html.Div(id = 'accessibility-pie-all', children = [
                
                html.Div([
                    html.Div(id = 'dp-access', children=[], style = {'order': '2'}),
                    html.Div(id = 'access-pie-all', children= [], style = {'order': '1', 'margin': 'auto'})], style = {'order': '1', 'display':'flex', 'flex-direction':'column', 'border-radius':'5px', 'height': '35vh', 'box-shadow': '0px 0px 15px rgba(0, 0, 0, 0.2)',
                                                                                                                       'border-radius':'5px', 'align-items':'center', 'backgroundColor': 'white', 'margin-right': '1vw', 'margin': 'auto', 'margin-left': '4vw'}),
                    
                html.Div(id = 'fields-pie-all', children = [], style = {'order': '2', 'backgroundColor': 'white', 'border-radius':'5px', 'height': '35vh', 'box-shadow': '0px 0px 15px rgba(0, 0, 0, 0.2)', 'margin': 'auto', 'margin-left': '1vw'})],
                     
                     style = {'order': '2', 'display': 'flex', 'flex-direction': 'row', 'align-items': 'center',
                              'align-content':'center'})],
                 
            style={'width': '95%', 'height':'30%', 'display': 'flex', 'width':'80vw',
                    'flex-direction': 'row', 'align-items': 'center',
                    'margin-top': '3vh','justify-content': 'space-evenly'}),
        
        html.Br(),
        html.Br(),
        
        html.Div([
            html.Div(id = 'active-authors-graph-all', children = [], style = {'order': '2', 'backgroundColor': 'white', 'border-radius':'5px', 'box-shadow': '0px 0px 15px rgba(0, 0, 0, 0.2)', 'margin-left': '2vw'}),
            html.Div(id = 'citations-graph-all', children = [], style = {'order': '1', 'backgroundColor': 'white', 'border-radius':'5px', 'box-shadow': '0px 0px 15px rgba(0, 0, 0, 0.2)', 'margin-right': '2vw'})],
            style={'width': '95%', 'height':'30%', 'display': 'flex',
                'flex-direction': 'row', 'align-items': 'center', 'margin': 'auto', 'width':'80vw',
                'margin-bottom': '3vh', 'justify-content': 'space-evenly'}),

        ],
        
        style = {'width': '85vw', 'display': 'flex',
                'flex-direction': 'column', 'align-items': 'center', 'margin': 'auto',
                'justify-content': 'space-evenly', 'border-radius': '5px', 'margin-bottom': '3vh'})
    
    if tab == 'tab-2-example-graph':
        return html.Div([
            html.Div([
                
                    html.Div([
                    html.Button('Reset view', id='bt-reset', className= 'reset-button'),
                    html.Div(id = 'dp-access-cytoscape', children = [], style={'order':'2'})], style={'order':'2', 'display':'flex', 'width':'44vw', 'flex-direction':'row', 'justify-content': 'space-between'}),
                    cyto.Cytoscape(
                        id='cytoscape-event-callbacks-1',
                        layout={'name': 'random', 'height': '58vh', 'width': '44vw'},
                        style = {'order': '3', 'height': '58vh', 'width': '44vw', 'margin': 'auto', 'margin-top': '5vh'},
                        stylesheet = [
                            {
                                'selector': 'label',
                                'style': {
                                    'content': 'data(label)',
                                    'color': 'rgba(60, 25, 240, 0.8)',
                                    'font-size':'14vh',
                                    'font-family':'Arial, sans serif',
                                    'background-color': 'rgba(60, 25, 240, 0.8)'
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
                                    'background-color': 'rgba(60, 25, 240, 0.8)'
                                }
                            },
                            {
                                'selector': '.collaboration',
                                'style': {
                                    'line-color': '#737373',
                                    'width': 1
                                }
                            }
                            ])],
                    
                style = {'order': '1', 'backgroundColor': 'white', 'display': 'flex', 'flex-direction': 'column',
                         'align-items': 'center', 'width': '55vw', 'height': '65vh', 'margin-bottom': '2vh', 'float': 'left', 'border-radius': '5px'}),
            
            html.Div(className= 'vl', style = {'order': '2'}),
            
            html.Div([
                    html.Div([
                            html.Div(id = 'author-info-1', style = {'width': '95%', 'height': '90%', 'margin':'auto'})],
                             style = {'order':'3', 'width':'95%', 'display': 'flex', 'flex-direction': 'row', 'align-items': 'center', 'margin': 'auto', 'justify-content': 'space-around'})],
                    
                style = {'order': '3', 'backgroundColor': 'white', 'display': 'flex', 'flex-direction': 'column', 'align-items': 'center',
                        'width': '30vw', 'height': '65vh', 'float': 'left', 'border-radius': '5px', 'margin': 'auto'})
    
    ], style={'backgroundColor': 'white','display': 'flex', 'flex-direction': 'row', 'align-items':'center', 'width': '85vw',
              'justify-content':'space-between', 'min-height':'70vh', 'box-shadow': '0px 0px 15px rgba(0, 0, 0, 0.2)',
              'margin': 'auto', 'border-radius': '5px', 'margin-bottom': '3vh'})
        
    if tab == 'tab-3-example-graph':
        return html.Div([

                html.Div([
                    
                    html.Button('Reset view', id='bt-reset-papers', className= 'reset-button'),
                    cyto.Cytoscape(
                        id='cytoscape-event-callbacks-2',
                        layout={'name': 'random', 'height': '58vh', 'width': '50vw'},
                        style={'order': '2', 'height': '58vh', 'width': '50vw'},
                        stylesheet = [
                            {
                                'selector': 'node',
                                'style': {
                                    'background-color': 'rgba(60, 25, 240, 0.8)',
                                    'height': '9vh',
                                    'width': '9vh'
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
                                    'line-color': '#737373',
                                    'width': 1
                                }
                            }
                            ])],
                    
                style = {'order': '1', 'width':'55vw', 'height': '65vh', 'display': 'flex',
                        'flex-direction': 'column', 'align-items': 'center',
                        'margin-bottom': '3vh', 'border-radius': '5px'}),
                
                html.Div(className= 'vl', style = {'order': '2'}),

                html.Div([
                        html.Div([
                            html.Div(id = 'paper-info-1', style = {'width': '95%', 'height': '90%', 'margin':'auto'})],
                        style = {'order': '2', 'width': '95%', 'height': '45vh', "margin": "auto", 'overflow-y':'auto', 'border-radius': '5px'})],
                    
                style = {'order': '3', 'width':'30vw', 'height': '65vh', 'display': 'flex',
                        'flex-direction': 'column', 'align-items': 'center',
                        'margin-bottom': '3vh', 'border-radius': '5px', 'margin':'auto'})],
            
            style = {'display': 'flex', 'flex-direction': 'row', 'align-items':'center', 'backgroundColor': 'white',
                     'justify-content':'space-between', 'min-height':'70vh', 'width': '85vw',
                     'margin': 'auto', 'border-radius': '5px', 'margin-bottom': '3vh'})

# Topic title
@app.callback(
    Output('topic', 'children'),
    Input('search-query', 'value'))
def display_topic(value):
    if value != None:
        return "Welcome researcher! 🧠"
    else:
        return "Welcome researcher! 🧠"

# Top flashcards -----------------------------------------------
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
    return dcc.Graph(figure=fig, style = {'width':'40vw', 'height':'45vh', 'border-radius': '5px'})

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
    return dcc.Graph(figure=fig, style = {'width':'40vw', 'height':'35vh', 'border-radius': '5px'})

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
    return dcc.Dropdown(id = 'dp-access-component', value = 'All', options = options, clearable=False, placeholder= 'Select a field of study', className= 'dp-access-piie')


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
    return dcc.Graph(className = 'access-pie', figure = fig, style={'order':'1', 'border-radius': '5px', 'width': '20vw', 'height':'35vh'})

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
    return dcc.Graph(figure=fig, style = {'width':'40vw', 'height':'45vh', 'border-radius': '5px', 'margin': 5})

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
    return dcc.Graph(figure=fig, style = {'width':'40vw', 'height':'45vh', 'border-radius': '5px', 'margin': 5})

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
    return dcc.Graph(figure=fig, style = {'width':'20vw', 'height':'40vh', 'border-radius': '5px'})

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
    return dcc.Graph(figure=fig, style = {'width':'40vw', 'height':'45vh', 'border-radius': '5px', 'margin': 5})

# Cytoscapes -------------------------------------------------------------------
@app.callback(
    Output('dp-access-cytoscape', 'children'),
    Input('store-initial-query-response', 'data'))
def create_accessibility_pie_all(data_res):
    dff_res = pd.DataFrame(data_res['data'])
    dff_res['result'] = 'direct'
    fields_of_study = dff_res['fieldsOfStudy'].tolist()
    res = [field for field in fields_of_study if isinstance(field, list)]
    flat_list_fields = utils.flatten_list(res)
    options = ['All'] + list(set(flat_list_fields))
    return dcc.Dropdown(id = 'dp-access-component_cytoscape', value = 'All', options = options, clearable=False, placeholder= 'Select a field of study', className= 'dp-access-pie')

@app.callback(
    Output('cytoscape-event-callbacks-1', 'elements'),
    Output('cytoscape-event-callbacks-1', 'zoom'),
    Input('store-initial-query-response', 'data'),
    Input('bt-reset', 'n_clicks'),
    Input('dp-access-component_cytoscape', 'value'),
    Input('cytoscape-event-callbacks-1', 'zoom'))
def generate_collaboration_network(data_res, n_clicks, filter, zoom):
    dff_res = pd.DataFrame(data_res['data'])
    dff_res['result'] = 'direct'
    if filter == 'All':
        elements = plots.generate_graph_elements_collab(dff_res)
    else:
        index_list = []
        for index, row in dff_res.iterrows():
            if isinstance(row.fieldsOfStudy, list):
                if filter in row.fieldsOfStudy:
                    index_list.append(index)
        dff_filtered = dff_res.loc[index_list]
        elements = plots.generate_graph_elements_collab(dff_filtered)
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
        paragraph = html.Div([html.Br(),
                     html.B(author_info['name'], style = {'font-size': '3vh', 'color': 'rgba(60, 25, 240, 0.8)'}), html.Br(),html.Br(),html.Br(),
                     html.Li([html.Span("Published ", style = {'font-size': '2vh', 'color': 'black'}), html.B(author_info['paperCount'], style = {'font-size': '3vh', 'color': 'rgba(60, 25, 240, 0.8)'}), html.Span(" papers.", style = {'font-size': '2vh', 'color': 'black'})], style = {'color': 'black', 'font-size': '3vh'}), html.Br(),html.Br(),
                     html.Li([html.Span("Received ", style = {'font-size': '2vh', 'color': 'black'}), html.B(author_info['citationCount'], style = {'font-size': '3vh', 'color': 'rgba(60, 25, 240, 0.8)'}), html.Span(" citations.", style = {'font-size': '2vh', 'color': 'black'})], style = {'color': 'black', 'font-size': '3vh'}), html.Br(),html.Br(),
                     html.Li([html.Span(f"h index: ", style = {'font-size': '2vh', 'color': 'black'}), html.B(author_info['hIndex'], style = {'font-size': '3vh', 'color': 'rgba(60, 25, 240, 0.8)'})], style = {'color': 'black', 'font-size': '3vh'}), html.Br(), html.Br(),
                     html.Li([html.A("Semantic Scholar profile", href = author_info['url'], target= '_blank', style = {'font-size': '2vh', 'color': 'rgba(60, 25, 240, 0.8)'})], style = {'color': 'black', 'font-size': '3vh'})],
                             style = {'margin':'auto'})

        return paragraph
    else:
        return html.P("Click on a node to display information about an author",
                           style = {'order': '2', 'font-size': '2vh', 'text-align':'center', 'width': '25vw', 'margin-top': '-10vh',
                                    'font-family': 'Courier New, monospace', 'color': 'rgba(3, 3, 3, 0.2)', 'margin': 'auto'})

# Retrieves info on paper
@app.callback(Output('paper-info-1', 'children'),
              Input('cytoscape-event-callbacks-2', 'tapNodeData'))
def displayTapNodeData(data):
    if data:
        paper_info = semantic_api.get_paper_info(data['id'])
        if 'paperId' in paper_info:
            if paper_info['isOpenAccess']:
                oa = ''
            else:
                oa = 'NOT'
            if paper_info['abstract'] == None:
                paper_info['abstract'] = 'No abstract available for this paper.'
            paragraph = html.Div([html.Br(), html.B(paper_info['title'], style = {'font-size': '3vh', 'color': 'rgba(60, 25, 240, 0.8)'}), html.Br(),html.Br(),
                                html.Li([html.Span("Published in ", style = {'font-size': '1.5vh', 'color': 'black'}), html.B(paper_info['year'], style = {'font-size': '1.5vh', 'color': 'rgba(60, 25, 240, 0.8)'})], style = {'color': 'black', 'font-size': '1.5vh'}),
                                html.Li([html.Span("Includes ", style = {'font-size': '1.5vh', 'color': 'black'}), html.B(paper_info['referenceCount'], style = {'font-size': '1.5vh', 'color': 'rgba(60, 25, 240, 0.8)'}), html.Span(" references.", style = {'font-size': '1.5vh', 'color': 'black'})], style = {'color': 'black', 'font-size': '1.5vh'}),
                                html.Li([html.Span("Received ", style = {'font-size': '1.5vh', 'color': 'black'}), html.B(paper_info['citationCount'], style = {'font-size': '1.5vh', 'color': 'rgba(60, 25, 240, 0.8)'}), html.Span(" citations.", style = {'font-size': '1.5vh', 'color': 'black'})], style = {'color': 'black', 'font-size': '1.5vh'}),
                                html.Li([html.Span("Is ", style = {'font-size': '1.5vh', 'color': 'black'}), html.B(oa, style = {'font-size': '1.5vh', 'color': 'rgba(60, 25, 240, 0.8)'}), html.Span(" open access.", style = {'font-size': '1.5vh', 'color': 'black'})], style = {'color': 'black', 'font-size': '1.5vh'}),
                                html.Li([html.A(' Semantic Scholar URL', href = paper_info['url'], target = '_blank', style = {'font-size': '1.5vh', 'color': 'rgba(60, 25, 240, 0.8)'})], style = {'color': 'black', 'font-size': '1.5vh'}), html.Br(),
                                html.B("Abstract", style = {'font-size': '3vh', 'color': 'rgba(60, 25, 240, 0.8)'}), html.Br(),
                                html.Span(paper_info['abstract'], style = {'font-size': '2vh', 'color': 'black'})], style = {'margin': 'auto'})
        else:
            paragraph = html.P("No info available for this paper", style = {'font-size': '1.5vh', 'color': 'rgba(60, 25, 240, 0.8)', 'margin': 'auto'})
        return paragraph
    else:
        return html.P("Click on a node to display information about a paper",
                           style = {'order': '2', 'font-size': '2vh', 'text-align':'center', 'width': '25vw',
                                    'font-family': 'Courier New, monospace', 'color': 'rgba(3, 3, 3, 0.2)', 'margin-top': '20vh'})

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)