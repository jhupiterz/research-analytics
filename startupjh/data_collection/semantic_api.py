#----------------------------------------------------------------------------------#
#      This code collects data about scientific papers using Semantic Scholar      # 
#                       visit https://api.semanticscholar.org/                     #
#----------------------------------------------------------------------------------#
#                                     ---Usage---                                  #
#                   Run the method get_papers_from_quey() followed by              #
#                             get_references_of_all_results()                      #
#----------------------------------------------------------------------------------#

import requests
import pandas as pd

from startupjh import utils
from startupjh.data_preprocessing import data_preprocess

def get_papers_from_query(search_query):
    url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={search_query}&limit=30&fields=url,title,abstract,authors,venue,year,referenceCount,citationCount,influentialCitationCount,isOpenAccess,fieldsOfStudy"
    response = requests.get(url).json()
    results_df = pd.DataFrame(response['data'])
    results_df['reference'] = build_references(results_df)
    results_df['first_author_id'] = build_first_author_id(results_df)
    results_df = data_preprocess.extract_key_words(results_df)
    total_results = response['total']
    return results_df, total_results

def get_references_from_paper(paper_id):
    url = f"https://api.semanticscholar.org/graph/v1/paper/{paper_id}/references?limit=50&fields=intents,isInfluential,paperId,url,title,abstract,venue,year,referenceCount,citationCount,influentialCitationCount,isOpenAccess,fieldsOfStudy,authors"
    response = requests.get(url).json()
    data = response['data']
    
    list_dict = []
    for elements in data:
        list_dict.append(elements['citedPaper'])
    
    references_df = pd.DataFrame(list_dict)
    references_df['citedBy'] = paper_id
    references_df['reference'] = build_references(references_df)
    references_df = data_preprocess.extract_key_words(references_df)
    return references_df

def get_references_of_all_results(results_df):
    all_references_df = get_references_from_paper(results_df['paperId'][0])
    for index, row in results_df[1:].iterrows():
        references_df = get_references_from_paper(row['paperId'])
        all_references_df = pd.concat([all_references_df,references_df])
    return all_references_df

def get_all_results_from_semantic_scholar():
    query = utils.get_user_input()
    search_query = utils.format_user_input(query)
    results_df, total_results = get_papers_from_query(search_query)
    all_references_df = get_references_of_all_results(results_df)
    return results_df, all_references_df, total_results, query

def build_references(df):
    ref_list = []
    for index, row in df.iterrows():
        if len(row.authors) == 0:
            ref = None
        elif len(row.authors) == 1:
            ref = row.authors[0]['name'] + ' (' + str(row.year) + ')'
        elif len(row.authors) == 2:
            ref = row.authors[0]['name'] + ', ' + row.authors[1]['name'] + ' (' + str(row.year) + ')'
        elif len(row.authors) > 2:
            ref = row.authors[0]['name'] + ' et al.' + ' (' + str(row.year) + ')'
        ref_list.append(ref)
    return ref_list

def build_first_author_id(df):
    author_id_list = []
    for index, row in df.iterrows():
        if len(row.authors) > 1:
            author_id = row.authors[0]['authorId']
        else:
            author_id = None
        author_id_list.append(author_id)
    return author_id_list
    
    
    