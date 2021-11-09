#--------------------------------------------------------------------------#
#    This code collects data about scientific papers using Unpaywall API   # 
#                 visit https://unpaywall.org/products/api                 #
#--------------------------------------------------------------------------#
#                                 ---Usage---                              #
#                                                                          #
#--------------------------------------------------------------------------#

from startupjh.utils import get_user_input
from startupjh.utils import format_user_input

import pandas as pd
import requests

def unpaywall_api():
    """Requests Unpaywall API and returns a dataframe of papers
       with the following columns: title, doi, genre, is_oa, 
       journal_is_oa, journal_name, published_date, publisher, authors"""
    query = get_user_input()
    search_query = format_user_input(query)

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
    return papers_df