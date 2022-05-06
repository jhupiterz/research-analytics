#--------------------------------------------------------------------------#
#          This code generates plots to be displayed in Dashboards         # 
#--------------------------------------------------------------------------#

# imports ------------------------------------------------------------------
from numpy.lib import utils
import utils
from datetime import date
import pandas as pd
from collections import Counter
import plotly.graph_objs as go
import plotly.express as px

# function definitions -----------------------------------------------------
# function names are self-explanatory --------------------------------------

def make_access_pie(df):
  oa_publications = df.groupby('isOpenAccess').count()
  #print(oa_publications)
  df_ = oa_publications
  fig = px.pie(df_, values='title', names= df_.index, color=df_.index, labels={'isOpenAccess': 'Open Access', 'title': 'Count'},
               color_discrete_map={'no data':'#eda109',
                                   'true':'#a8fffe',
                                   'false':'#fa3960'})
  
  fig.update_layout(
    showlegend=False,
    title = "<span style='font-size: 22px;'><b>Open access publications<b></span>", title_x=0.5,
    font=dict(
        family="Courier New, monospace",
        size=14,
        color="white"
    ),
    paper_bgcolor = "#101126",
    plot_bgcolor = "#101126")
  return fig

def make_fields_pie(df):
    test_list = df.fieldsOfStudy.tolist()
    res = [i for i in test_list if i]
    flat_list_fields = utils.flatten_list(res)
    
    most_common_fields = Counter(flat_list_fields).most_common()
    most_common_fields_df = pd.DataFrame(most_common_fields, columns=["field", "occurence"])
    
    fig = px.pie(most_common_fields_df.loc[0:7], values='occurence', names= 'field')

    fig.update_layout(
    showlegend=True,
    title = "<span style='font-size: 22px;'><b>Fields of Study<b></span>", title_x=0.5,
    font=dict(
        family="Courier New, monospace",
        size=14,
        color="white"
    ),
    paper_bgcolor = "#101126",
    plot_bgcolor = "#101126")
    return fig

def make_yearly_popularity(df):
  popularity = df.groupby('year').count()['citationCount'] + df.groupby('year').sum()['citationCount']
  fig = px.line(df, x=df.groupby('year').count()['citationCount'].index,
              y=popularity, title='Populatiry Index')
  fig.update_layout(title = "<span style='font-size: 22px;'><b>Evolution of popularity<b></span>", title_x=0.5,
                      font=dict(
                                family="Courier New, monospace",
                                size=12,
                                color="white"
      ),
      paper_bgcolor = "#101126",
      plot_bgcolor = "#101126")
    
  fig.update_traces(marker_color='#eda109')
  fig.update_xaxes(title="Year", range= [df.year.min() - 5, date.today().year + 5])
  fig.update_yaxes(title="Popularity Indey", range= [0, 1.1* popularity.max()])
  return fig

def make_pub_per_year_line(df):
  #print(df.groupby(['year', 'result'], as_index=False).count())
  fig = px.line(df, x=df.groupby(['year', 'result'], as_index=False).count().year,
              y=df.groupby(['year', 'result'], as_index=False).count()['citationCount'], color = df.groupby(['year', 'result'], as_index=False).count()['result'], title='Publications per year')
  fig.update_layout(title = "<span style='font-size: 22px;'><b>Publications per Year<b></span>", title_x=0.5,
                      font=dict(
                                family="Courier New, monospace",
                                size=12,
                                color="white"
      ),
      paper_bgcolor = "#101126",
      plot_bgcolor = "#101126")
    
  fig.update_traces(marker_color='#eda109')
  fig.update_xaxes(title="Year", range= [1950, date.today().year + 5])
  fig.update_yaxes(title="Number of Publications", range= [0, 1.1 * df[df.year>1950].groupby('year').count()['citationCount'].max()])
  return fig

def make_pub_per_year(df, which_api):
  if which_api == 'semantic_scholar':
    fig = go.Figure(data=[go.Bar(x=df.groupby('year').count()['citationCount'].index,
                             y= df.groupby('year').count()['citationCount'],
                             texttemplate="%{y}",
                             textposition="outside",
                             textangle=0)])
  else:
    fig = go.Figure(data=[go.Bar(x=df.groupby('published_year').count()['citation_count'].index,
                              y= df.groupby('published_year').count()['citation_count'],
                              texttemplate="%{y}",
                              textposition="outside",
                              textangle=0)])
  fig.update_layout(title = "<span style='font-size: 22px;'><b>Publications per Year<b></span>", title_x=0.5,
                    font=dict(
                              family="Courier New, monospace",
                              size=12,
                              color="white"
    ),
    paper_bgcolor = "#101126",
    plot_bgcolor = "#101126")
  
  fig.update_traces(marker_color='#eda109')
  if which_api == 'semantic_scholar':
    fig.update_xaxes(title="Year", range= [df.year.min() - 5, date.today().year + 5])
    fig.update_yaxes(title="Number of Publications", range= [0, 1.1* df.groupby('year').count()['citationCount'].max()])
  else:
    fig.update_xaxes(title="Year", range= [df.published_year.min() - 5, date.today().year + 5])
    fig.update_yaxes(title="Number of Publications", range= [0, 1.1* df.groupby('published_year').count()['citation_count'].max()])
  return fig

def make_citations_per_year_line(df):
  #print(df.groupby(['year', 'result'], as_index=False).sum())
  fig = px.line(df, x=df.groupby(['year', 'result'], as_index=False).sum().year,
              y=df.groupby(['year', 'result'], as_index=False).sum()['citationCount'], color=df.groupby(['year', 'result'], as_index=False).sum()['result'], title='Citations per year')
  fig.update_layout(title = "<span style='font-size: 22px;'><b>Citations per Year<b></span>", title_x=0.5,
                      font=dict(
                                family="Courier New, monospace",
                                size=12,
                                color="white"
      ),
      paper_bgcolor = "#101126",
      plot_bgcolor = "#101126")
    
  fig.update_traces(marker_color='#eda109')
  fig.update_xaxes(title="Year", range= [1950, date.today().year + 5])
  fig.update_yaxes(title="Number of Citations", range= [0, 1.1* df[df.year>1950].groupby('year').sum()['citationCount'].max()])
  return fig

def make_citations_per_year(df, which_api):
  if which_api == 'semantic_scholar':
    fig = go.Figure(data=[go.Bar(x=df.groupby('year').sum()['citationCount'].index,
                             y= df.groupby('year').sum()['citationCount'],
                             texttemplate="%{y}",
                             textposition="outside",
                             textangle=0)])
  else:
    fig = go.Figure(data=[go.Bar(x=df.groupby('published_year').sum()['citation_count'].index,
                              y= df.groupby('published_year').sum()['citation_count'],
                              texttemplate="%{y}",
                              textposition="outside",
                              textangle=0)])
  fig.update_layout(title = "<span style='font-size: 22px;'><b>Citations per Year<b></span>", title_x=0.5,
                    font=dict(
                              family="Courier New, monospace",
                              size=12,
                              color="white"
    ),
    paper_bgcolor = "#101126",
    plot_bgcolor = "#101126")
  fig.update_traces(marker_color='#eda109')
  if which_api == 'semantic_scholar':
    fig.update_xaxes(title="Year", range= [df.year.min() - 5, date.today().year + 5])
    fig.update_yaxes(title="Number of Publications", range= [0, 1.1* df.groupby('year').sum()['citationCount'].max()])
  else:
    fig.update_xaxes(title="Year", range= [df.published_year.min() - 5, date.today().year + 5])
    fig.update_yaxes(title="Number of Publications", range= [0, 1.1* df.groupby('published_year').sum()['citation_count'].max()])
  return fig

def make_active_authors(df):
    authors_list = []
    for index, row in df.iterrows():
        for dict_ in row.authors:
            authors_list.append(dict_['name'])
    most_active_authors = Counter(authors_list).most_common()
    most_active_authors_df = pd.DataFrame(most_active_authors, columns=["author", "occurence"])
    fig = go.Figure(data=[go.Bar(x=most_active_authors_df[0:10].author,
                              y= most_active_authors_df[0:10].occurence,
                              texttemplate="%{y}",
                              textposition="outside",
                              textangle=0)])
    fig.update_layout(title = "<span style='font-size: 22px;'><b>Most active authors<b></span>", title_x=0.5,
                    font=dict(
                              family="Courier New, monospace",
                              size=12,
                              color="white"
    ),
    paper_bgcolor = "#101126",
    plot_bgcolor = "#101126")

    fig.update_traces(marker_color='#eda109')
    fig.update_xaxes(title="Authors")
    fig.update_yaxes(title="Number of Publications", range= [0, 1.1* most_active_authors_df.occurence.max()])
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
  query = query.split()
  key_word_list = tuple(flatten_list)
  cleaned_list = [ x for x in key_word_list if query[0] not in x ]
  for i in range(1,len(query)):
    cleaned_list = [ x for x in cleaned_list if query[i] not in x ]
  #cleaned_tuple = tuple(key_word_list)
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
  fig.update_layout(
    title = "<span style='font-size: 22px;'><b>Top key words<b></span>", title_x=0.5,
    font=dict(
        family="Courier New, monospace",
        size=12,
        color="white"
    ),
    paper_bgcolor = "#101126",
    plot_bgcolor = "#101126")
  fig.update_traces(marker_color='#eda109')
  fig.update_yaxes(title="Number of occurences", range= [0, 1.1* top_key_words_plot['occurence'].max()])
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

def get_top_publisher(df):
  top_publisher_pubs = df.groupby('publisher').count().sort_values('citation_count', ascending=False)
  top_publisher = top_publisher_pubs.index[0]
  if top_publisher == 'no data':
    top_publisher = top_publisher_pubs.index[1]
  return top_publisher

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

def generate_collab_network_df(df):
  authors_list_of_list = []
  ids_list_of_list = []
  for index, row in df.iterrows():
      authors_list = []
      ids_list = []
      for dict_ in row.authors:
          authors_list.append(dict_['name'])
          ids_list.append(dict_['authorId'])
      authors_list_of_list.append(authors_list)
      ids_list_of_list.append(ids_list)
  authors_combinations = []
  ids_combinations = []
  for authors in authors_list_of_list:
      res = [(a, b) for idx, a in enumerate(authors) for b in authors[idx + 1:]]
      authors_combinations.append(res)
  for ids in ids_list_of_list:
      rex = [(a, b) for idx, a in enumerate(ids) for b in ids[idx + 1:]]
      ids_combinations.append(rex)
  flat_authors_combinations = utils.flatten_list(authors_combinations)
  flat_ids_combinations = utils.flatten_list(ids_combinations)
  most_common_collab = Counter(flat_authors_combinations).most_common(50)
  most_common_collab_ids = Counter(flat_ids_combinations).most_common(50)
  unpacked_most_collab = [(a, b, c) for (a, b ), c in most_common_collab]
  unpacked_most_collab_ids = [(a, b, c) for (a, b ), c in most_common_collab_ids]
  nx_df = pd.DataFrame(unpacked_most_collab, columns=['author1', 'author2', 'weight'])
  nx_id_df = pd.DataFrame(unpacked_most_collab_ids, columns=['id1', 'id2', 'weight1'])
  collabs_df = pd.concat([nx_df, nx_id_df], axis=1)
  collabs_df['author1'] = list(zip(collabs_df.author1, collabs_df.id1))
  collabs_df['author2'] = list(zip(collabs_df.author2, collabs_df.id2))
  collabs_df.drop(['id1', 'id2', 'weight1'], axis = 1, inplace = True)
  return collabs_df

def generate_graph_elements_collab(df):
    nx_df = generate_collab_network_df(df)
    unique_top_authors = list(set(nx_df.author1.unique().tolist() + nx_df.author2.unique().tolist()))
    nodes_list = [{'data': {'id': unique_top_authors[0][1], 'label': unique_top_authors[0][0]}, 'classes': 'author'}]
    for element in unique_top_authors[1:]:
        nodes_list.append({'data': {'id': element[1], 'label': element[0]}, 'classes': 'author'})
    edges_list = [{'data': {'source': nx_df['author1'][0][1], 'target': nx_df['author2'][0][1]}, 'classes': 'collaboration'}]
    for index, row in nx_df.iterrows():
        edges_list.append({'data': {'source': row.author1[1], 'target': row.author2[1]}, 'classes': 'collaboration'})
    elements = nodes_list + edges_list
    return elements

def generate_ref_network_df(df1, df2):
    """df1 = all_references_df
     df2 = results_df"""
    ref1 = []
    ref2 = []
    for index, row in df1.iterrows():
        ref1.append((row.reference,row['paperId']))
        ref2.append(("".join(df2.reference[df2.paperId == row['citedBy']]), row['citedBy']))
    ref_network_df = pd.DataFrame(
    {'ref1': ref1,
     'ref2': ref2
    })
    return ref_network_df

def generate_graph_elements_network(df1, df2):
    ref_network_df = generate_ref_network_df(df1, df2)
    unique_refs = list(set(ref_network_df.ref1.unique().tolist()))
    unique_results = list(set(ref_network_df.ref2.unique().tolist()))
    nodes_refs = [{'data': {'id': unique_refs[0][1], 'label': unique_refs[0][0], 'classes': 'ref'}}]
    nodes_results = [{'data': {'id': unique_results[0][1], 'label': unique_results[0][0], 'classes': 'res'}}]
    nodes_list = nodes_refs + nodes_results
    for element in unique_refs[1:]:
        nodes_list.append({'data': {'id': element[1], 'label': element[0], 'classes': 'ref'}})
    for element in unique_results[1:]:
        nodes_list.append({'data': {'id': element[1], 'label': element[0], 'classes': 'res'}})
    edges_list = [{'data': {'source': ref_network_df['ref1'][0][1], 'target': ref_network_df['ref2'][0][1]}, 'classes': 'citation'}]
    for index, row in ref_network_df.iterrows():
        edges_list.append({'data': {'source': row.ref1[1], 'target': row.ref2[1]}, 'classes': 'citation'})
    elements = nodes_list + edges_list
    #print(elements)
    return elements