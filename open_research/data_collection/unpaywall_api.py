#--------------------------------------------------------------------------#
#    This code collects data about scientific papers using Unpaywall API   # 
#                 visit https://unpaywall.org/products/api                 #
#--------------------------------------------------------------------------#

from data_preprocessing.data_preprocess import extract_key_words

import pandas as pd
import requests

def unpaywall_api(search_query):
    """Requests Unpaywall API and returns a dataframe of papers
       with the following columns: title, doi, genre, is_oa, 
       journal_is_oa, journal_name, published_date, publisher, authors"""
    # query = get_user_input()
    # search_query = format_user_input(query)

    url = 	f"https://api.unpaywall.org/v2/search?query={search_query}&email=julie.hartz13@gmail.com"
    response = requests.get(url).json()
    list_papers = response["results"]

    papers = []
    for paper in list_papers:
        if paper['response']['title']:
            title = paper['response']['title']
        else: 
            title = ""
        if paper['response']['doi']:
            doi = paper['response']['doi']
        else:
            doi = ""
        if paper['response']['genre']:
            genre = paper['response']['genre']
        else: 
            genre = ""
        if paper['response']['is_oa']:
            is_oa = paper['response']['is_oa']
        else:
            is_oa = False
        if paper['response']['journal_is_oa']:
            journal_is_oa = paper['response']['journal_is_oa']
        else: 
            journal_is_oa = False
        if paper['response']['journal_name']:
            journal_name = paper['response']['journal_name']
        else: 
            journal_name = ""
        if paper['response']['published_date']:
            published_date = paper['response']['published_date']
        else:
            published_date = ""
        if paper['response']['publisher']:
            publisher = paper['response']['publisher']
        else:
            publisher = ""
        if paper['response']['z_authors']:
            authors = paper['response']['z_authors']
        else:
            authors = ""
        
        paper_dict = {"title": title,
                    "doi": doi,
                    "genre": genre,
                    "is_oa": is_oa,
                    "journal_is_oa": journal_is_oa,
                    "journal_name": journal_name,
                    "published_date": published_date,
                    "publisher": publisher,
                    "authors": authors}
        papers.append(paper_dict)
        papers_df = pd.DataFrame(papers)
        
    authors = []
    affiliations = []
    for index, row in papers_df.iterrows():
        authors_list = []
        affiliation_list = []
        for author in row['authors']:
            affiliation = []
            if ('given' in author) and ('family' in author):
                author_fullname = author['given'] + " " + author['family']
            elif ('given' not in author) and ('family' in author):
                author_fullname = author['family']
            elif ('given' in author) and ('family' not in author):
                author_fullname = author['given']
            else:
                author_fullname = author['name']
            if 'affiliation' in author:
                for e in author['affiliation']:
                    affiliation.append(e['name'])
            #else: 
                #affiliation = np.nan
            authors_list.append(author_fullname)
            affiliation_list.append(affiliation)
        authors.append(authors_list)
        affiliations.append(affiliation_list)
    papers_df.authors = authors
    papers_df['affiliations'] = affiliations
    papers_df = extract_key_words(papers_df)
    return papers_df