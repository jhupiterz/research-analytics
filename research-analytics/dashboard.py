#--------------------------------------------------------------------------#
#                   This code makes use of all other functions of          #
#                      the package to build a Dash Web App                 # 
#--------------------------------------------------------------------------#

# imports ------------------------------------------------------------------
from pydoc import classname
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
                            src="/assets/web.png",
                            alt="research intelligence"
                        ),
                        html.H3("research analytics")
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
            dcc.Tabs(id="tabs-example-graph", value = 'tab-1-example-graph', className= "tabs",
                        children=[
                dcc.Tab(label='📊  Search results  📊', value='tab-1-example-graph',
                        className= "single-tab", selected_className= "single-tab-selected"),
                dcc.Tab(label='🤝  Author network  🤝', value='tab-2-example-graph',
                        className= "single-tab", selected_className= "single-tab-selected"),
                dcc.Tab(label='🌐  Paper network  🌐', value='tab-3-example-graph',
                        className= "single-tab", selected_className= "single-tab-selected")
                ])
            ],
                        className= "tabs-container"),
        html.Br(),
        html.Div(id='tabs-content-example-graph'))
    else:
        return html.Div(
            [
                html.Hr(),
                html.P("👇  Or check out the latest blog posts about data-driven academia  👇"), html.Br(),
                html.Div([
                html.A(
                        href="https://medium.com/@juhartz/are-scholarly-papers-really-the-best-way-to-disseminate-research-f8d85d3eee62",
                        children=[
                            html.Img(
                                alt="Link to my twitter",
                                src="assets/blogpost_1.png",
                                className="zoom"
                            )
                        ], target= '_blank', className= "blog-post-1"
                    ),
                html.A(
                        href="https://medium.com/@juhartz/what-makes-a-research-paper-impactful-a40f33206fd1",
                        children=[
                            html.Img(
                                alt="Link to my twitter",
                                src="assets/blogpost_2.png",
                                className='zoom'
                            )
                        ], target= '_blank', className= "blog-post-2"
                    )
                        ],className= "blog-posts")],
            className= "start-page")
    
@app.callback(Output('tabs-content-example-graph', 'children'),
              Input('tabs-example-graph', 'value'))
def render_tab_content(tab):
    if tab == 'tab-1-example-graph':
        return html.Div([
        html.Div([
            dcc.Loading(id = "loading-icon-1",
                children=[html.Div(id = 'keywords-graph-all', children= [], className= "keywords-graph")], type = 'default', className= "loading-keywords"),
            
            html.Div(id = 'accessibility-pie-all', children = [
                
                html.Div([
                    html.Div(id = 'dp-access', children=[], style = {'order': '2'}),
                    html.Div(id = 'access-pie-all', children= [], style = {'order': '1', 'margin': 'auto'})],
                         className= "accessibility-graph"),
                    
                html.Div(id = 'fields-pie-all', children = [], className= "fields-pie-graph")],
                     
                     className= "fields-pie-and-dropdown")],
                 
            className= "tab-1-upper-graphs"),
        
        html.Br(),
        html.Br(),
        
        html.Div([
            html.Div(id = 'active-authors-graph-all', children = [], className= "active-authors-graph"),
            html.Div(id = 'citations-graph-all', children = [], className= "citations-graph")],
            className= "tab-1-lower-graphs"),
        ],
        
        className= "tab-1")
    
    if tab == 'tab-2-example-graph':
        return html.Div([
            html.Div([
                
                    html.Div([
                    html.Button('Reset view', id='bt-reset', className= 'reset-button'),
                    html.Div(id = 'dp-access-cytoscape', children = [], style={'order':'2'})],
                             className= "dropdown-and-button-cyto-1"),
                    cyto.Cytoscape(
                        id='cytoscape-event-callbacks-1',
                        layout={'name': 'random', 'height': '58vh', 'width': '44vw'},
                        className= "cyto-1",
                        stylesheet = [
                            {
                                'selector': 'label',
                                'style': {
                                    'content': 'data(label)',
                                    'color': 'rgba(60, 25, 240, 0.8)',
                                    'font-size':'14vh',
                                    'font-family':'Arial, sans serif',
                                }
                            },
                            {
                                'selector': 'node',
                                'style': {
                                    'label': 'data(label)'
                                } 
                            },
                            {
                                'selector': '[selected ^= "True"]',
                                'style': {
                                'background-color': 'green',
                                'line-color': 'green'
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
                    
                className= "cyto-1-and-button-container"),
            
            html.Div(className= 'vl', style = {'order': '2'}),
            
            html.Div([
                    html.Div([
                            html.Div(id = 'author-info-1', className= "author-info")],
                             className= "author-info-container")],
                    
                className= "author-info-big-container")
    
    ], className= "tab-2")
        
    if tab == 'tab-3-example-graph':
        return html.Div([

                html.Div([
                    
                    html.Button('Reset view', id='bt-reset-papers', className= 'reset-button'),
                    cyto.Cytoscape(
                        id='cytoscape-event-callbacks-2',
                        layout={'name': 'random', 'height': '58vh', 'width': '50vw'},
                        style={'order':'2','height': '58vh', 'width': '50vw'},
                        #className= "cyto-2",
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
                    
                className= "cyto-2-and-button-container"),
                
                html.Div(className= 'vl', style = {'order': '2'}),

                html.Div([
                        html.Div([
                            html.Div(id = 'paper-info-1', className= "paper-info")],
                        className= "paper-info-container")],
                    
                className= "paper-info-big-container")],
            
            className= "tab-3")

# Topic title
@app.callback(
    Output('topic', 'children'),
    Input('search-query', 'value'))
def display_topic(value):
    if value != None:
        return "Welcome researcher!"
    else:
        return "Welcome researcher!"

# Plots and graphs ----------------------------------------------
# keywords
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
    return dcc.Graph(figure=fig, className= "keywords-plotly")

# loading states for keyword graphs
@app.callback(Output('loading-icon-1', 'children'),
              Input('keywords-graph-res', 'children'))

@app.callback(Output('loading-icon-2', 'children'),
              Input('keywords-graph-ref', 'children'))

# accessibility

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
    return dcc.Dropdown(id = 'dp-access-component', value = 'All',
                        options = options, clearable=False,
                        placeholder= 'Select a field of study', className= 'dp-access-piie')


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
    return dcc.Graph(figure = fig, className= "access-pie-plotly")

# publications per year
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
    return dcc.Graph(figure=fig, className= "pub-graph-plotly")

# citations per year
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
    return dcc.Graph(figure=fig, className= "pub-graph-plotly")

# fields of study
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
    return dcc.Graph(figure=fig, className= "fields-pie-plotly")

# most active authors
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
    return dcc.Graph(figure=fig, className = "pub-graph-plotly")

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
    return dcc.Dropdown(id = 'dp-access-component_cytoscape', value = 'All',
                        options = options, clearable=False,
                        placeholder= 'Select a field of study', className= 'dp-access-pie')

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
        print(data)
        author_info = semantic_api.get_author_info(data['id'])
        paragraph = html.Div([
                     html.B(author_info['name']), html.Br(),html.Br(),
                     html.Span("Published "), html.B(author_info['paperCount']), html.Span(" papers."), html.Br(),html.Br(),
                     html.Span("Received "), html.B(author_info['citationCount']), html.Span(" citations."), html.Br(),html.Br(),
                     html.Span(f"h index: "), html.B(author_info['hIndex']), html.Br(), html.Br(),
                     html.A("Semantic Scholar profile", href = author_info['url'], target= '_blank')],
                             className = "author-info-text"),
        return paragraph
    else:
        return html.P("Click on a node to display information about an author",
                           className= "author-info-default-text")

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
            paragraph = html.Div([html.Br(), html.B(paper_info['title']), html.Br(),html.Br(),
                                html.Li([html.Span("Published in "), html.B(paper_info['year'])]),
                                html.Li([html.Span("Includes "), html.B(paper_info['referenceCount']), html.Span(" references.")]),
                                html.Li([html.Span("Received "), html.B(paper_info['citationCount']), html.Span(" citations.")]),
                                html.Li([html.Span("Is "), html.B(oa), html.Span(" open access.", style = {'font-size': '1.5vh', 'color': 'black'})]),
                                html.Li([html.A(' Semantic Scholar URL', href = paper_info['url'], target = '_blank')]), html.Br(),
                                html.B("Abstract"), html.Br(),
                                html.Span(paper_info['abstract'])],
                                className= "paper-info-text")
        else:
            paragraph = html.P("No info available for this paper", className= "paper-info-default-no-info")
        return paragraph
    else:
        return html.P("Click on a node to display information about a paper",
                           className= "paper-info-default-text")

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)