# Code creating a dashboard using plotly.dash

import dash
import dash_daq as daq
import dash_core_components as dcc
import dash_html_components as html
from startupjh.data import scraper_api

def generate_top():
    df = scraper_api("automation+container+terminal")
    cols = ['title', "year", "citations", "cited_by_url"]
    col_names = ['Title', 'Year', 'Number of citations', 'Citing papers']
    class_names = ['title','year','citations','citing']
    df = df.loc[df['state']=='India',:]
    rows = []
    for i in range(4):
        arrow = '&#8595;' if (i==0) and (df[cols[4]].iloc[0] > 0) else '&#8593;'
        rows.append(html.Th([
            html.P(col_names[i]),
            html.H4(df[cols[i]].iloc[0],className=class_names[i]),
            dcc.Markdown(f"{arrow} {df[cols[i+4]].iloc[0]}",
                className=class_names[i])
        ]))
    return html.Table([
        html.Thead(rows)
    ], id='top-details')


app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
server = app.server

app.layout = html.Div([
    html.Div([
        html.H1('Topic : automation container terminal'),
    ], id='header-div'),
    html.Br(),
    html.Div(
            generate_top()
        ),
    html.Br(),
    dcc.Dropdown(
            id = 'state-dropdown',
            options=[{'label':state,'value':state} for state in states],
            value='India'
    ),
    html.Br(),
    html.Div([
        dcc.Tabs(id="tabs", value='active', children=[
            dcc.Tab(label='Active', value='active'),
            dcc.Tab(label='Confirmed', value='confirmed'),
            dcc.Tab(label='Recovered', value='recoveries'),
            dcc.Tab(label='Deceased', value='deaths'),
        ]),
    dcc.Graph(id='india-graph'),
    html.Br(),
    html.Div([
        daq.ToggleSwitch(
            id='my-toggle-switch',
            label = ['Daily','Cumulative'],
            value=True
            ),
    ], id='toggle-switch-div'),
    html.Br()
    ], id='tabs_plus_graph'),
    html.Br(),
    html.H3('All State/UT Stats'),
    html.Br(),
    generate_table(df_states,max_rows=40),

], id='main-div')

if __name__ == '__main__':
    app.run_server(host='0.0.0.0')