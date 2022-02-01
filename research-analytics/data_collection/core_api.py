#--------------------------------------------------------------------------#
#      This code collects data about scientific papers using CORE API      # 
#                     visit https://api.core.ac.uk/docs/v3                 #
#--------------------------------------------------------------------------#

# imports ------------------------------------------------------------------
from data_preprocessing.data_preprocess import extract_key_words
import pandas as pd
import requests

# function definitions -----------------------------------------------------
def core_api(search_query):
    """what it does: queries CORE API and builds a dataframe with the data collected
       arguments: take a search query (str) as argument
       returns: a dataframe containing information collected about the papers"""
    
    # query
    API_KEY = "BX8LxuP2c6CUn0tEIVlrJvisFqMdYehZ"
    entityType = "outputs"
    url = f"https://api.core.ac.uk/v3/search/{entityType}?q={search_query}&limit=5&stats=true&apiKey={API_KEY}"
    response = requests.get(url).json()
    results = response['results']
    
    # retrieve info of interest and handling KeyErrors
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
        
        # build dictionary
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
    
    # sort out authors list into desired format
    authors = []
    for index, row in papers_df.iterrows():
        author_list = []
        for author in row.authors:
            if "," in author['name']:
                author_fullname = author['name'].split(",")
                author_name = author_fullname[1].strip()+" "+author_fullname[0]
            else:
                author_name = author['name']
            author_list.append(author_name)
        authors.append(author_list)
    papers_df.authors = authors
    
    # sort out published date into desired format
    published_date = []
    for index, row in papers_df.iterrows():
        if row.published_date:
            date = row.published_date.rstrip('T00:00:00+00:00')
        else:
            date = ""
        published_date.append(date)
    papers_df.published_date = published_date
    
    # extract key words, rename and drop columns
    papers_df = extract_key_words(papers_df)
    papers_df = papers_df.rename(columns={'download_url':'link'})
    papers_df.drop(labels=['tags'], axis=1, inplace=True)
    return papers_df