#--------------------------------------------------------------------------#
#      This code collects data about scientific papers using DOAJ API      # 
#                     visit https://api.core.ac.uk/docs/v3                 #
#--------------------------------------------------------------------------#
#                                 ---Usage---                              #
#              Just run the method core_api() and it will ask for          #
#               user input and return a up to 50 paper dataframe           #                                         #
#--------------------------------------------------------------------------#

from startupjh.utils import get_user_input
from startupjh.utils import format_user_input

import pandas as pd
import requests

def core_api():
    query = get_user_input()
    search_query = format_user_input(query)

    API_KEY = "BX8LxuP2c6CUn0tEIVlrJvisFqMdYehZ"
    entityType = "outputs"
    url = f"https://api.core.ac.uk/v3/search/{entityType}?q={search_query}&limit=50&apiKey={API_KEY}"

    response = requests.get(url).json()
    results = response['results']

    papers = []
    for result in results:
        if 'authors' in result:
            author = result['authors']
        else:
            author = ""
        if 'abstract' in result:
            abstract = result['abstract']
        else:
            abstract = ""
        if 'documentType' in result:
            document_type = result['documentType']
        else:
            document_type = ""
        if 'doi' in result:
            doi = result['doi']
        else:
            doi = ""
        if 'downloadUrl' in result:
            download_url = result['downloadUrl']
        else:
            download_url = ""
        if 'fullText' in result:
            full_text = result['fullText']
        else:
            full_text = ""
        if 'title' in result:
            title = result['title']
        else:
            title = ""
        if 'language' in result:
            language = result['language']
        else: 
            language = ""
        if 'publishedDate' in result:
            published_date = result['publishedDate']
        else:
            published_date = ""
        if 'publisher' in result:
            publisher = result['publisher']
        else: 
            publisher = ""
        if 'references' in result:
            references = result['references']
        else:
            references = ""
        if 'tags' in result:
            tags = result['tags']
        else:
            tags = ""
        paper_dict = {"authors": author,
                    "abstract": abstract,
                    "document_type": document_type,
                    "doi": doi,
                    "download_url": download_url,
                    "full_text": full_text,
                    "title": title,
                    "language": language,
                    "published_date": published_date,
                    "publisher": publisher,
                    "references": references,
                    "tags": tags
        }
        papers.append(paper_dict)
    papers_df = pd.DataFrame(papers)
    return papers_df