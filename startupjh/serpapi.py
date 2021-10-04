# This code aims to collect data about scientific papers using Serp API 
# https://serpapi.com
# Need to figure out how to scrape more than 1 page with SerpAPI

from serpapi import GoogleSearch
import pandas as pd

def get_key_words():
    """get user input for topic to search"""
    search_query = input("Enter key words: ")
    return search_query

def serpapi():
    """scrapes google scholar using SerpAPI
       output is a dataframe with following columns: 
       [title, result_id, link, snippet, resources_title, resources_link, 
        citation_count, cites_id, versions, cluster_id]"""
                                
    query = get_key_words()
    
    params = {
        "engine": "google_scholar",
        "q": query,
        "api_key": "bd9ae4d322ca6af163e484036232d68bbfc7385d22eb5b3553fbdecb46509c20"
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    organic_results = results['organic_results']

    papers = []

    for paper in organic_results:
        title = paper["title"]
        result_id = paper["result_id"]
        if "type" in paper:
            file_format = paper["type"]
        else:
            file_format = "no data"
        link = paper["link"]
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

        paper_dict = {"title": title,
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
        papers_df = pd.DataFrame(papers)
    return papers_df

def serpapi_full_cite(df):
    """Scrapes Google scholar for full citations (Cite snippet)
       Iterates over a given df[result_id] and extracts full MLA citation
       Output is a dataframe with [full_citation] column"""
    full_citations = []
    for _, row in df.iterrows():
        params = {
        "engine": "google_scholar_cite",
        "q": row.result_id,
        "api_key": "bd9ae4d322ca6af163e484036232d68bbfc7385d22eb5b3553fbdecb46509c20"
        }

        search = GoogleSearch(params)
        results = search.get_dict()
        full_citation = results['citations'][0]["snippet"]
        full_citations.append(full_citation)
    df["full_citation"] = full_citations
    return df