# Code creating a dashboard using plotly.dash

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table

import pandas as pd

from startupjh import utils
from startupjh import plots
from startupjh import data_preprocess

# Instanciate web app with Dash
app = dash.Dash(__name__)

# Defines colors to be used in HTML or CSS below
# colors = {
#     'background': '#111111',
#     'text': '#7FDBFF'
# }

# Load data
papers_df = utils.load_from_csv("../data/more_papers.csv")
citing_papers_df = utils.load_from_csv("../data/more_citing_papers.csv")

# Get most cited papers
most_cited_papers_df = pd.DataFrame(papers_df.sort_values(by="citation_count", ascending=False).iloc[0:3].authors + " " + papers_df.sort_values(by="citation_count", ascending=False).iloc[0:3].year.apply(str))
most_cited_papers_df["Citations"] = papers_df.sort_values(by="citation_count", ascending=False).iloc[0:3].citation_count
most_cited_papers_df.columns = ["Citation", "Number of citations"]

#Get most active journals
active_journals_primary = data_preprocess.get_most_active_journal(papers_df).head(2)
active_journals_citing = data_preprocess.get_most_active_journal(citing_papers_df).head(4)
most_active_journals_primary = active_journals_primary[active_journals_primary["occurence"] == max(active_journals_primary.occurence)]
most_active_journals_citing = active_journals_citing[active_journals_citing["occurence"] == max(active_journals_citing.occurence)]

# Create plots
fig1 = plots.plot_citations_per_year(papers_df, citing_papers_df)
fig2 = plots.plot_publications_per_year(papers_df, citing_papers_df)
fig3 = plots.plot_most_common_words(papers_df, citing_papers_df)

# Dashboard layout (basicall HTML written in python)
app.layout = html.Div([
    html.H1("Topic: automation container terminal", style={'backgroundColor': '#202020', 'text-align': 'center', 'font-family': 'Avantgarde, TeX Gyre Adventor, URW Gothic L, sans-serif', 'color': 'white'}),
        html.Div(className="row",
                 style={'backgroundColor': '#202020'},
                 children = [
                     html.Div(className= "six columns",
                             style={'backgroundColor': '#202020'},
                    children = [
                        html.H3('Most cited papers', style={'font-family': 'Avantgarde, TeX Gyre Adventor, URW Gothic L, sans-serif', 'color': 'white', 'text_align': 'center'}),
                        html.Div(
                        dash_table.DataTable(
                                            id='table1',
                                            columns=[{"name": i, "id": i} for i in most_cited_papers_df.columns],
                                            data=most_cited_papers_df.to_dict('records'),
                                            fill_width=False
                                        )
            )]),
                        html.Div(className= "six columns",
                                style={'backgroundColor': '#202020'},
                    children = [
                        html.H3('Most publishing journals - primary results', style={'font-family': 'Avantgarde, TeX Gyre Adventor, URW Gothic L, sans-serif', 'color': 'white', 'text_align': 'center'}),
                        html.Div(
                        dash_table.DataTable(
                                            id='table2',
                                            columns=[{"name": i, "id": i} for i in most_active_journals_primary.columns],
                                            data=most_active_journals_primary.to_dict('records'),
                                            fill_width=False
                                        )
            )]),
                        html.Div(className= "six columns",
                                style={'backgroundColor': '#202020'},
                    children = [
                        html.H3('Most publishing journals - citing papers', style={'font-family': 'Avantgarde, TeX Gyre Adventor, URW Gothic L, sans-serif', 'color': 'white', 'text_align': 'center'}),
                        html.Div(
                        dash_table.DataTable(
                                            id='table3',
                                            columns=[{"name": i, "id": i} for i in most_active_journals_citing.columns],
                                            data=most_active_journals_citing.to_dict('records'),
                                            fill_width=False
                                        )
            )]),
                     
                    html.Div(className= "six columns",
                             style={'backgroundColor': '#202020'},
                    children = [
                        html.H3('Citations per year', style={'font-family': 'Avantgarde, TeX Gyre Adventor, URW Gothic L, sans-serif', 'color': 'white', 'text_align': 'center'}),
                        html.Div(
                        dcc.Graph(id='fig1', figure=fig1)
            )]),

                    html.Div(className="six columns",
                             style={'backgroundColor': '#202020'},
                    children = [
                        html.H3('Publications per year', style={'font-family': 'Avantgarde, TeX Gyre Adventor, URW Gothic L, sans-serif', 'color': 'white', 'text_align': 'center'}),
                        html.Div(
                        dcc.Graph(id='fig2', figure=fig2)
            )]),

                    html.Div(className="six columns",
                             style={'backgroundColor': '#202020'},
                    children = [
                        html.H3('Most common words', style={'font-family': 'Avantgarde, TeX Gyre Adventor, URW Gothic L, sans-serif', 'color': 'white', 'text_align': 'center'}),
                        html.Div(
                        dcc.Graph(id='fig3', figure=fig3)
            )])
    ])
])

# CSS code - from external source (url template) or can write up our own
app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

# Runs the app on local server
if __name__ == '__main__':
    app.run_server(debug=True)