#--------------------------------------------------------------------------#
#             This code generates plots to be used in Dashboards           # 
#--------------------------------------------------------------------------#
#                                ---Usage---                               #
#              Each function returns a plotly graph object figure          #
#--------------------------------------------------------------------------#
from numpy.lib import utils
from startupjh import utils
from datetime import date
import pandas as pd
import networkx as nx
from pyvis.network import Network
from collections import Counter
import plotly.graph_objs as go
import plotly.express as px

def make_access_pie(df):
  oa_publications = df.groupby('journal_is_oa').count()#.sort_values('citation_count', ascending=False)
  df_ = oa_publications
  fig = px.pie(df_, values='title', names= df_.index)
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
  fig.update_xaxes(title="Year", range= [df.published_year.min(), date.today().year + 5])
  fig.update_yaxes(title="Number of Publications")
  return fig

def make_citations_per_year(df):
  fig = go.Figure(data=[go.Bar(x=df.groupby('published_year').sum()['citation_count'].index,
                             y= df.groupby('published_year').sum()['citation_count'],
                             texttemplate="%{y}",
                             textposition="outside",
                             textangle=0)])
  fig.update_layout(title = f"Citations per Year", title_x=0.5)
  fig.update_xaxes(title="Year", range= [df.published_year.min(), date.today().year + 5])
  fig.update_yaxes(title="Number of Publications")
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
  fig.update_yaxes(title="Number of citations")
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
  fig.update_yaxes(title="Number of publications")
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
  fig.update_yaxes(title="Number of publications")
  return fig

def make_top_publishers_cites(df):
  top_publisher_citations = df.groupby('publisher').sum().sort_values('citation_count', ascending=False)
  top_publisher_citations.drop(labels=['no data'], axis=0, inplace=True)
  top_publisher_citations_plot = top_publisher_citations[top_publisher_citations['citation_count'] > 50]
  fig = go.Figure(data=[go.Bar(x=top_publisher_citations_plot.index,
                             y= top_publisher_citations_plot['citation_count'],
                             texttemplate="%{y}",
                             textposition="outside",
                             textangle=0)])
  fig.update_layout(title = f"Top publishers", title_x=0.5)
  fig.update_yaxes(title="Number of citations")
  return fig

def make_top_key_words(df, query):
  """query should be the list of keywords from user input"""
  list_keywords = []
  for index, row in df.iterrows():
      list_keywords.append(row.key_words)
  flatten_list = utils.flatten_list(list_keywords)
  # print(query, type(query))
  query = query.split()
  key_word_list = tuple(flatten_list)
  cleaned_list = [ x for x in key_word_list if query[0] not in x ]
  for i in range(1,len(query)):
    cleaned_list = [ x for x in cleaned_list if query[i] not in x ]
  cleaned_tuple = tuple(cleaned_list)
  key_words_sorted = Counter(cleaned_tuple).most_common()
  top_key_words = pd.DataFrame(key_words_sorted, columns=["key_word", "occurence"])
  top_key_words = top_key_words.sort_values(by="occurence", ascending=False)
  top_key_words_plot = top_key_words[0:15]
  
  fig = go.Figure(data=[go.Bar(x=top_key_words_plot['key_word'],
                             y= top_key_words_plot['occurence'],
                             texttemplate="%{y}",
                             textposition="outside",
                             textangle=0)])
  fig.update_layout(title = f"Top key words", title_x=0.5)
  fig.update_yaxes(title="Number of occurences")
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

def make_top_pub_box(df):
  
  top_publisher_pubs = df.groupby('publisher').count().sort_values('citation_count', ascending=False)
  top_publisher = top_publisher_pubs.index[0]
  if top_publisher == 'no data':
    top_publisher = top_publisher_pubs.index[1]
  
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
      y=[0.3],
      mode="text",
      text=top_publisher,
      textfont_size=26,
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
  return fig

def generate_collab_network_df(df):
  authors_combinations = []
  for authors in df.authors:
      res = [(a, b) for idx, a in enumerate(authors) for b in authors[idx + 1:]]
      authors_combinations.append(res)
  flat_authors_combinations = utils.flatten_list(authors_combinations)
  most_common_collab = Counter(flat_authors_combinations).most_common(50)
  unpacked_most_collab = [(a, b, c) for (a, b ), c in most_common_collab]
  nx_df = pd.DataFrame(unpacked_most_collab, columns=['author1', 'author2', 'weight'])
  # G = nx.from_pandas_edgelist(nx_df,
  #                           source='author1',
  #                           target='author2',
  #                           edge_attr='weight'
  # )
  return nx_df

def make_top_authors(df):
  flat_author_list = utils.flatten_list(df.authors.tolist())
  top_authors_df = pd.DataFrame(Counter(flat_author_list).most_common(50), columns=['author', 'occurence'])
  fig = go.Figure(data=[go.Bar(x=top_authors_df['author'][0:5],
                             y= top_authors_df['occurence'][0:5],
                             texttemplate="%{y}",
                             textposition="outside",
                             textangle=0)])
  fig.update_layout(title = f"Top key words", title_x=0.5)
  fig.update_yaxes(title="Number of occurences")
  return fig

def generate_graph_elements(df):
  nx_df = generate_collab_network_df(df)
  unique_top_authors = list(set(nx_df.author1.unique().tolist() + nx_df.author2.unique().tolist()))
  nodes_list = [{'data': {'id': unique_top_authors[0], 'label': unique_top_authors[0]}}]
  for element in unique_top_authors[1:]:
      nodes_list.append({'data': {'id': element, 'label': element}})
  edges_list = [{'data': {'source': nx_df['author1'][0], 'target': nx_df['author2'][0]}}]
  for index, row in nx_df.iterrows():
      edges_list.append({'data': {'source': row.author1, 'target': row.author2}})
  elements = nodes_list + edges_list
  return elements