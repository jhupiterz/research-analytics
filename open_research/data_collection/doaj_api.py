#--------------------------------------------------------------------------#
#      This code collects data about scientific papers using DOAJ API      # 
#                 visit https://unpaywall.org/products/api                 #
#--------------------------------------------------------------------------#
#                                 ---Usage---                              #
#               Just run the method doaj_api() and it will ask for         #
#               user input and return a up to 50 paper dataframe           #                                         #
#--------------------------------------------------------------------------#

from utils import get_user_input
from utils import format_user_input

import pandas as pd
import requests

def doaj_api(search_query):
    # query = get_user_input()
    # search_query = format_user_input(query)

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
        papers.append(paper_dict)
    papers_df = pd.DataFrame(papers)
    authors = []
    affiliations = []
    for index, row in papers_df.iterrows():
        author_list = []
        affiliation_list = []
        for author in row.author:
            author_list.append(author['name'])
            if 'affiliation' in author:
                affiliation_list.append(author['affiliation'])
            else:
                affiliation_list.append("")
        authors.append(author_list)
        affiliations.append(affiliation_list)
    papers_df.author = authors
    papers_df['affiliations'] = affiliations
    journal_name = []
    journal_is_oa = []
    publisher = []
    for index, row in papers_df.iterrows():
        journal_name.append(row.journal['title'])
        journal_is_oa.append(row.journal['is_oa'])
        publisher.append(row.journal['publisher'])
    papers_df['journal_name'] = journal_name
    papers_df['journal_is_oa'] = journal_is_oa
    papers_df['publisher'] = publisher
    # Get published date, by default the day of the month is set to 1
    published_date = []
    for index, row in papers_df.iterrows():
        if row.pub_month:
            if len(row.pub_month) == 1:
                month = "0"+row.pub_month
            else: 
                month = row.pub_month
        else:
            month = "06"
        date = row.pub_year+"-"+month+"-"+"01"
        published_date.append(date)
    papers_df['published_date'] = published_date
    # Get number of pages
    number_of_pages = []
    for index, row in papers_df.iterrows():
        if (row.start_page) and (row.end_page):
            if (row.start_page.isdigit()) and (row.end_page.isdigit()):
                number_pages = int(row.end_page) - int(row.start_page)
        else:
            number_pages = ""
        number_of_pages.append(number_pages)
    papers_df['number_of_pages'] = number_of_pages
    papers_df.drop(labels = ['pub_year', 'pub_month', 'start_page', 'end_page', 'journal'], axis=1, inplace = True)
    papers_df = papers_df.rename(columns={'keywords': 'key_words', 'author': 'authors'})
    return papers_df