#--------------------------------------------------------------------------#
#             This code generates plots to be used in Dashboards           # 
#--------------------------------------------------------------------------#
#                                ---Usage---                               #
#              Each function returns a plotly graph object figure          #
#--------------------------------------------------------------------------#

from plotly.subplots import make_subplots
import plotly.graph_objs as go

from startupjh import data_preprocess

# Number of publications per year
def plot_publications_per_year(df1, df2):
    fig = make_subplots(rows=1, cols=2,
                        y_title='Number of publications',
                        subplot_titles=('Primary papers',  'Citing papers'))

    fig.add_trace(
        go.Bar(x=df1.groupby("year", as_index=False).count()['year'],
               y=df1.groupby("year", as_index=False).count()['paper_id']),
               row=1, col=1
    )

    fig.add_trace(
        go.Bar(x=df2.groupby("year", as_index=False).count()['year'],
               y=df2.groupby("year", as_index=False).count()['paper_id']),
               row=1, col=2
    )

    fig.update_xaxes(
            title_text = "Year",
            range = [1990, 2024],
            tick0 = 1990,
            dtick = 5,
            ticks = 'outside'
    )

    fig.update_yaxes(ticks = 'outside')

    fig.update_layout(showlegend=False, template="seaborn")

    return fig

# Number of citations per year
def plot_citations_per_year(df1, df2):
    fig = make_subplots(rows=1, cols=2,
                        y_title='Number of citations',
                        subplot_titles=('Primary papers',  'Citing papers'))

    fig.add_trace(
        go.Bar(x=df1.groupby(["year"], as_index=False).citation_count.sum()["year"],
               y=df1.groupby(["year"], as_index=False).citation_count.sum()["citation_count"]),
               row=1, col=1
    )

    fig.add_trace(
        go.Bar(x=df2.groupby(["year"], as_index=False).citation_count.sum()["year"],
               y=df2.groupby(["year"], as_index=False).citation_count.sum()["citation_count"]),
               row=1, col=2
    )

    fig.update_xaxes(
            title_text = "Year",
            range = [1990, 2024],
            tick0 = 1990,
            dtick = 5,
            ticks = 'outside'
    )

    fig.update_yaxes(ticks = 'outside')

    fig.update_layout(showlegend=False, template="seaborn")

    return fig

def plot_most_common_words(df1, df2):
    
    key_words_papers_df = data_preprocess.get_most_common_key_words(df1)
    key_words_citing_papers_df = data_preprocess.get_most_common_key_words(df2)
    
    
    fig = make_subplots(rows=1, cols=2,
                        vertical_spacing=0.1,
                        y_title = "occurences",
                        subplot_titles=('Primary papers',  'Citing papers'))

    fig.add_trace(
        go.Bar(x= key_words_papers_df[key_words_papers_df["occurence"] > 1]["key_word"],
               y= key_words_papers_df[key_words_papers_df["occurence"] > 1]["occurence"],
               marker=dict(
                            color='rgba(247, 129, 191, 0.6)',
                            line=dict(color='rgba(246, 78, 139, 1.0)', width=3)
                          )),
               row=1, col=1
    )

    fig.add_trace(
        go.Bar(x= key_words_citing_papers_df[key_words_citing_papers_df["occurence"] > 5]["key_word"],
               y= key_words_citing_papers_df[key_words_citing_papers_df["occurence"] > 5]["occurence"],
               marker=dict(
                            color='rgba(51, 51, 255, 0.6)',
                            line=dict(color='rgb(51, 51, 255, 1.0)', width=3)
                          )),
               row=1, col=2
    )
    
    #fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                  #marker_line_width=1.5)

    fig.update_xaxes(title_text = "Key words", gridcolor = "rgb(102,102,102)")

    fig.update_yaxes(ticks = 'outside', gridcolor= "rgb(102,102,102)")

    fig.update_layout(showlegend=False,
                      template="seaborn",
                      width=1200, height=600,
                      plot_bgcolor = "rgb(204,204,204)",
                      title_text = "Most common key words")

    return fig