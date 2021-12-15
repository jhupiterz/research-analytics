#--------------------------------------------------------------------------#
#             This code generates plots to be used in Dashboards           # 
#--------------------------------------------------------------------------#
#                                ---Usage---                               #
#              Each function returns a plotly graph object figure          #
#--------------------------------------------------------------------------#
import pandas as pd
from collections import Counter
import plotly.graph_objs as go
import plotly.express as px

def make_access_pie(df):
  oa_publications = df.groupby('journal_is_oa').count()#.sort_values('citation_count', ascending=False)
  df_ = oa_publications
  fig = px.pie(df_.groupby('journal_is_oa').count(), values='title', names= df_.index)
  fig.update_layout(title = f"Open Access publications", title_x=0.5)
  return fig

def make_pub_per_year(df):
  fig = go.Figure(data=[go.Bar(x=df.groupby('published_year').count()['citation_count'].index,
                             y= df.groupby('published_year').count()['citation_count'],
                             texttemplate="%{y}",
                             textposition="outside",
                             textangle=0)])
  fig.update_layout(title = f"Publications per Year", title_x=0.5)
  fig.update_traces(marker_color='#d8b3ff', marker_line_color='#d8b3ff',
                    marker_line_width=1.5)
  fig.update_xaxes(title="Year", range=[1993, 2023])
  fig.update_yaxes(title="Number of Publications")
  return fig

def make_citations_per_year(df):
  fig = go.Figure(data=[go.Bar(x=df.groupby('published_year').sum()['citation_count'].index,
                             y= df.groupby('published_year').sum()['citation_count'],
                             texttemplate="%{y}",
                             textposition="outside",
                             textangle=0)])
  fig.update_layout(title = f"Citations per Year", title_x=0.5)
  fig.update_xaxes(title="Year", range=[1993, 2023])
  fig.update_yaxes(title="Number of Publications", range=[0, 360])
  return fig

def make_top_cited_journals(df):
  top_journals_citations = df.groupby('journal_name').sum().sort_values('citation_count', ascending=False)
  top_journals_citations_plot = top_journals_citations[top_journals_citations['citation_count'] > 100]
  fig = go.Figure(data=[go.Bar(x=top_journals_citations_plot.index,
                             y= top_journals_citations_plot['citation_count'],
                             texttemplate="%{y}",
                             textposition="outside",
                             textangle=0)])
  fig.update_layout(title = f"Top cited journals", title_x=0.5)
  fig.update_yaxes(title="Number of citations", range=[0,400])
  return fig

def make_top_publishing_journals(df):
  top_journals_pubs = df.groupby('journal_name').count().sort_values('citation_count', ascending=False)
  top_journals_pubs_plot = top_journals_pubs[top_journals_pubs['title'] >= 2]
  fig = go.Figure(data=[go.Bar(x=top_journals_pubs_plot.index,
                             y= top_journals_pubs_plot['citation_count'],
                             texttemplate="%{y}",
                             textposition="outside",
                             textangle=0)])
  fig.update_layout(title = f"Top publishing journals", title_x=0.5)

  # Update xaxis properties
  #fig.update_xaxes(title="Journal")

  # Update yaxis properties
  fig.update_yaxes(title="Number of publications", range=[0,4])
  return fig

def make_top_publishers_pub(df):
  top_publisher_pubs = df.groupby('publisher').count().sort_values('citation_count', ascending=False)
  top_publisher_pubs_plot = top_publisher_pubs[top_publisher_pubs['title']>3][1:]
  fig = go.Figure(data=[go.Bar(x=top_publisher_pubs_plot.index,
                             y= top_publisher_pubs_plot['title'],
                             texttemplate="%{y}",
                             textposition="outside",
                             textangle=0)])
  fig.update_layout(title = f"Top publishers", title_x=0.5)
  fig.update_yaxes(title="Number of publications", range=[0,15])
  return fig

def make_top_publishers_cites(df):
  top_publisher_citations = df.groupby('publisher').sum().sort_values('citation_count', ascending=False)
  top_publisher_citations.drop(labels=['no data'], axis=0, inplace=True)
  top_publisher_citations_plot = top_publisher_citations[top_publisher_citations['citation_count'] > 200]
  fig = go.Figure(data=[go.Bar(x=top_publisher_citations_plot.index,
                             y= top_publisher_citations_plot['citation_count'],
                             texttemplate="%{y}",
                             textposition="outside",
                             textangle=0)])
  fig.update_layout(title = f"Top publishers", title_x=0.5)
  fig.update_yaxes(title="Number of citations", range=[0,1000])
  return fig

def make_top_key_words(df):
  list_keywords = []
  for index, row in df.iterrows():
      list_keywords.append(row.key_words)
  key_word_list = list(sum(list_keywords, ()))
  cleaned_list_from_kw1 = [ x for x in key_word_list if 'container' not in x ]
  cleaned_list_from_kw2 = [ x for x in cleaned_list_from_kw1 if 'automat' not in x ]
  cleaned_list = [ x for x in cleaned_list_from_kw2 if 'terminal' not in x ]
  key_words_sorted = Counter(cleaned_list).most_common()
  top_key_words = pd.DataFrame(key_words_sorted, columns=["key_word", "occurence"])
  top_key_words_plot = top_key_words[top_key_words['occurence'] >= 5]
  
  fig = go.Figure(data=[go.Bar(x=top_key_words_plot['key_word'],
                             y= top_key_words_plot['occurence'],
                             texttemplate="%{y}",
                             textposition="outside",
                             textangle=0)])
  fig.update_layout(title = f"Top key words", title_x=0.5)
  fig.update_yaxes(title="Number of occurences", range=[0,12])
  return fig

def make_first_pub_box(df):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
            x=[0, 0, 1, 1], y=[0, 1.4, 1.4, 0], fill="toself", fillcolor='white', mode='lines',
            line=dict(color="white")
        ))

    fig.add_trace(go.Scatter(
        x=[0.5],
        y=[1],
        mode="text",
        text=["Research topic active since"],
        textfont_size=18,
        textposition="top center"
    ))

    fig.add_trace(go.Scatter(
        x=[0.5],
        y=[0.07],
        mode="text",
        text=[int(df.published_year.min())],
        textfont_size=60,
        textposition="top center"
    ))

    fig.update_xaxes(visible=False)   
    fig.update_yaxes(visible=False)
    fig.update_layout(
        margin=go.layout.Margin(
        l=0, #left margin
        r=0, #right margin
        b=0, #bottom margin
        t=0, #top margin
        ),
        width = 300,
        height = 150,
        showlegend=False,
        plot_bgcolor='#d8b3ff',
        paper_bgcolor='#d8b3ff')
    #fig.show()
    return fig

def make_latest_pub_box(df):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
            x=[0, 0, 1, 1], y=[0, 1.4, 1.4, 0], fill="toself", fillcolor='white', mode='lines',
            line=dict(color="white")
        ))

    fig.add_trace(go.Scatter(
        x=[0.5],
        y=[1],
        mode="text",
        text=["Latest pub. published in"],
        textfont_size=18,
        textposition="top center"
    ))

    fig.add_trace(go.Scatter(
        x=[0.5],
        y=[0.07],
        mode="text",
        text=[int(df.published_year.max())],
        textfont_size=60,
        textposition="top center"
    ))

    fig.update_xaxes(visible=False)   
    fig.update_yaxes(visible=False)
    fig.update_layout(
        margin=go.layout.Margin(
        l=0, #left margin
        r=0, #right margin
        b=0, #bottom margin
        t=0, #top margin
        ),
        width = 300,
        height = 150,
        showlegend=False,
        plot_bgcolor='#d8b3ff',
        paper_bgcolor='#d8b3ff')
    #fig.show()
    return fig

def make_top_pub_box():
    fig = go.Figure()

    fig.add_trace(go.Scatter(
            x=[0, 0, 1, 1], y=[0, 1.4, 1.4, 0], fill="toself", fillcolor='white', mode='lines',
            line=dict(color="white")
        ))

    fig.add_trace(go.Scatter(
        x=[0.5],
        y=[1],
        mode="text",
        text=["Top publisher:"],
        textfont_size=18,
        textposition="top center"
    ))

    fig.add_trace(go.Scatter(
        x=[0.5],
        y=[0.07],
        mode="text",
        text=['IEEE'],
        textfont_size=60,
        textposition="top center"
    ))
    
    fig.update_xaxes(visible=False)   
    fig.update_yaxes(visible=False)
    fig.update_layout(
        margin=go.layout.Margin(
        l=0, #left margin
        r=0, #right margin
        b=0, #bottom margin
        t=0, #top margin
        ),
        width = 300,
        height = 150,
        showlegend=False,
        plot_bgcolor='#d8b3ff',
        paper_bgcolor='#d8b3ff')
    #fig.show()
    return fig