#--------------------------------------------------------------------------#
#      This code collects data about scientific papers using Serp API      # 
#                         visit https://serpapi.com                        #
#--------------------------------------------------------------------------#

# imports ------------------------------------------------------------------
from serpapi import GoogleSearch
from data_preprocessing.data_preprocess import extract_key_words
from data_preprocessing.data_preprocess import extract_pub_info
import pandas as pd

# function definitions -----------------------------------------------------
def serpapi_og_results(query):
    """what it does: scrapes INITIAL results from google scholar and builds a dataframe
       arguments: takes a search query (str) as argument
       returns: a dataframe containing the data collected about the papers"""
    
    # query
    params = {
        "engine": "google_scholar",
        "q": query,
        "api_key": "bd9ae4d322ca6af163e484036232d68bbfc7385d22eb5b3553fbdecb46509c20",
        "num": 20
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    organic_results = results['organic_results']

    # retrieve info of interest and handling KeyErrors
    papers = []
    i = 0
    
    for paper in organic_results:
        paper_id = i
        title = paper["title"]
        result_id = paper["result_id"]
        if "type" in paper:
            file_format = paper["type"]
        else:
            file_format = "no data"
        if "link" in paper:
            link = paper["link"]
        else:
            link = "no data"
        snippet = paper["snippet"]
        if "resources" in paper:
            resources_title = paper["resources"][0]["title"]
            resources_link = paper["resources"][0]["link"]
        else:
            resources_title = "no data"
            resources_link = "no data"
        if "inline_links" in paper:
            if "cited_by" in paper["inline_links"]:
                cites_id = paper["inline_links"]["cited_by"]["cites_id"]
                citation_count = paper["inline_links"]["cited_by"]["total"]
            else: 
                citation_count = 0
                cites_id = "no data"
            if "versions" in paper["inline_links"]:
                versions = paper["inline_links"]["versions"]["total"]
                cluster_id = paper["inline_links"]["versions"]["cluster_id"]
            else: 
                versions = "no data"
                cluster_id = "no data"

        # build dictionary
        paper_dict = {"paper_id": paper_id,
                    "title": title,
                    "result_id": result_id,
                    "link": link,
                    "snippet": snippet, 
                    "resources_title": resources_title,
                    "resources_link": resources_link, 
                    "citation_count": citation_count,
                    "cites_id": cites_id,
                    "versions": versions,
                    "cluster_id": cluster_id}
        papers.append(paper_dict)
        i = i + 1
    papers_df = pd.DataFrame(papers)
    return papers_df

def serpapi_full_cite(query):
    """what it does: scrapes Google scholar for the full citations
       arguments: takes a search query (str) as argument
       returns: returns a dataframe containing a 'full_citation' column"""
    
    # scrape INITIAL results
    df = serpapi_og_results(query)
    
    # iterate on INITIAL results df to retrieve full citations of each paper
    full_citations = []
    for _, row in df.iterrows():
        params = {
        "engine": "google_scholar_cite",
        "q": row.result_id,
        "api_key": "bd9ae4d322ca6af163e484036232d68bbfc7385d22eb5b3553fbdecb46509c20"
        }

        search = GoogleSearch(params)
        results = search.get_dict()
        full_citation = results['citations'][2]["snippet"]
        full_citations.append(full_citation)
    df["full_citation"] = full_citations
    df = extract_key_words(df)
    df = extract_pub_info(df)
    journal_name = []
    for element in df.pub_info:
        if ' (' in element:
            split_info = element.split(' (')
        else:
            split_info = element.split('. ')
        journal_name.append(split_info[0])
    df['journal_name'] = journal_name
    published_date = []
    for pub_year in df.year:
        date = pub_year+"-06-01"
        published_date.append(date)
    df['published_date'] = published_date
    df.drop(labels=["versions", "cluster_id", "pub_info", 'paper_id', 'year', 'result_id', 'resources_title', 'resources_link'], axis=1, inplace = True)
    df = df.rename(columns={'resources_link':'link'})
    return df

def serpapi_cited_by_list(df):
    """what it does: scrapes the list of papers citing the INITIAL results
       arguments: takes the df containing the INITIAL results
       returns: a new dataframe containg all the papers citing the INITIAL papers"""
    
    # iterates over INITIAL df to retrieve the  list of papers citing each INITIAL paper
    j = 0
    i = 0
    
    # query
    citing_papers = []
    for _, row in df.iterrows():
        if row.cites_id != "no data":
            params = {
                "engine": "google_scholar",
                "cites": row.cites_id,
                "api_key": "bd9ae4d322ca6af163e484036232d68bbfc7385d22eb5b3553fbdecb46509c20"
                }
            
            search = GoogleSearch(params)
            results = search.get_dict()
            organic_results = results['organic_results']
            
            papers = []

            # retrieve info of interest and handle KeyErrors
            for paper in organic_results:
                paper_id = i
                citing_paper_id = j
                title = paper["title"]
                result_id = paper["result_id"]
                if "type" in paper:
                    file_format = paper["type"]
                else:
                    file_format = "no data"
                if "link" in paper:
                    link = paper["link"]
                else:
                    link = "no data"
                if "snippet" in paper:
                    snippet = paper["snippet"]
                else:
                    snippet = "no data"
                if "resources" in paper:
                    resources_title = paper["resources"][0]["title"]
                    resources_link = paper["resources"][0]["link"]
                else:
                    resources_title = "no data"
                    resources_link = "no data"
                if "inline_links" in paper:
                    if "cited_by" in paper["inline_links"]:
                        cites_id = paper["inline_links"]["cited_by"]["cites_id"]
                        citation_count = paper["inline_links"]["cited_by"]["total"]
                    else: 
                        citation_count = 0
                        cites_id = "no data"
                    if "versions" in paper["inline_links"]:
                        versions = paper["inline_links"]["versions"]["total"]
                        cluster_id = paper["inline_links"]["versions"]["cluster_id"]
                    else: 
                        versions = "no data"
                        cluster_id = "no data"

                # build dictionary
                paper_dict = {"paper_id": paper_id,
                            "citing_paper_id": citing_paper_id,
                            "title": title,
                            "result_id": result_id,
                            "link": link,
                            "snippet": snippet, 
                            "resources_title": resources_title,
                            "resources_link": resources_link, 
                            "citation_count": citation_count,
                            "cites_id": cites_id,
                            "versions": versions,
                            "cluster_id": cluster_id}
                papers.append(paper_dict)
                i = i + 1
            j = j + 1
            citing_papers.append(papers)
    flatList = [ item for elem in citing_papers for item in elem]
    citing_papers_df = pd.DataFrame(flatList)
    return citing_papers_df