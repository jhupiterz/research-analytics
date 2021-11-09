#--------------------------------------------------------------------------#
#      This code collects data about scientific papers using DOAJ API      # 
#                 visit https://unpaywall.org/products/api                 #
#--------------------------------------------------------------------------#
#                                 ---Usage---                              #
#               Just run the method doaj_api() and it will ask for         #
#               user input and return a up to 50 paper dataframe           #                                         #
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
        if 'journal' in paper['bibjson']:
            if 'volume' in paper['bibjson']['journal']:
                journal_volume = paper['bibjson']['journal']['volume']
            else:
                journal_volume = ""
            if 'number' in paper['bibjson']['journal']:
                journal_issue = paper['bibjson']['journal']['number']
            else:
                journal_issue = ""
            if 'country' in paper['bibjson']['journal']:
                journal_country = paper['bibjson']['journal']['country']
            else:
                journal_country = ""
            if 'license' in paper['bibjson']['journal']:
                journal_is_oa = paper['bibjson']['journal']['license'][0]['open_access']
            else:
                journal_is_oa = ""
            if 'publisher' in paper['bibjson']['journal']:
                publisher = paper['bibjson']['journal']['publisher']
            else:
                publisher = ""
            if 'language' in paper['bibjson']['journal']:
                journal_language = paper['bibjson']['journal']['language']
            else:
                journal_language = ""
            if 'title' in paper['bibjson']['journal']:
                journal_title = paper['bibjson']['journal']['title'] 
            else:
                journal_title = ""
            journal = {"volume": journal_volume,
                            "issue": journal_issue,
                            "country": journal_country,
                            "is_oa": journal_is_oa,
                            "publisher": publisher,
                            "language": journal_language,
                            "title": journal_title}
        else:
            journal = ""
        if 'keywords' in paper['bibjson']:
            keywords = paper['bibjson']['keywords']
        else:
            keywords = ""
        if 'month' in paper['bibjson']:
            pub_month = paper['bibjson']['month']
        else:
            pub_month = ""
        if 'start_page' in paper['bibjson']:
            start_page = paper['bibjson']['start_page']
        else:
            start_page = ""
        if 'end_page' in paper['bibjson']:
            end_page = paper['bibjson']['end_page']
        else:
            end_page = ""
        if paper['bibjson']['year']:
            pub_year = paper['bibjson']['year']
        else:
            pub_year = ""
        if paper['bibjson']['author']:
            author = paper['bibjson']['author']
        else: 
            author = ""
        if paper['bibjson']['link']:
            link = paper['bibjson']['link'][0]['url']
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
                        "keywords": keywords,
                        "author": author,
                        "link": link,
                        "pub_year": pub_year,
                        "pub_month": pub_month,
                        "start_page": start_page,
                        "end_page": end_page,
                        "abstract": abstract}
        print(paper_dict)
        papers.append(paper_dict)
    papers_df = pd.DataFrame(papers)
    return papers_df