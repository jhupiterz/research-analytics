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

def doaj_api():
    query = get_user_input()
    search_query = format_user_input(query)

    url = f"https://doaj.org/api/search/articles/{search_query}?page=1&pageSize=60"
    response = requests.get(url).json()

    papers = []
    for paper in response['results']:
        if paper['bibjson']['journal']:
            journal = paper['bibjson']['journal']
        else:
            journal = ""
        if paper['bibjson']['year']:
            pub_year = paper['bibjson']['year']
        else:
            pub_year = ""
        if paper['bibjson']['author']:
            author = paper['bibjson']['author']
        else: 
            author = ""
        if paper['bibjson']['link']:
            link = paper['bibjson']['link']
        else:
            link = ""
        if paper['bibjson']['abstract']:
            abstract = paper['bibjson']['abstract']
        else:
            abstract = ""
        if paper['bibjson']['title']:
            title = paper['bibjson']['title']
        else:
            title = ""
            
        paper_dict = {"title": title,
                        "journal": journal,
                        "author": author,
                        "link": link,
                        "pub_year": pub_year,
                        "abstract": abstract}
        papers.append(paper_dict)
    papers_df = pd.DataFrame(papers)
    return papers_df