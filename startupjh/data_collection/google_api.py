#--------------------------------------------------------------------------#
#      This code collects data about scientific papers using Serp API      # 
#                         visit https://serpapi.com                        #
#--------------------------------------------------------------------------#
#                                 ---Usage---                              #
# To get the primary results of a Google Scholar search run the following: #
#                   primaryResults = serpapi_full_cite()                   #
#      To get the papers citing the primary results run the following:     #
#            citing_papers = serpapi_cited_by_list(primaryResults)         #
#                                                                          #
#    N.B. the second command will only run if the first one has been run   #
#--------------------------------------------------------------------------#

from serpapi import GoogleSearch
from startupjh import utils
import pandas as pd

def serpapi_og_results():
    """scrapes google scholar using SerpAPI
       output is a dataframe with following columns: 
       [title, result_id, link, snippet, resources_title, resources_link, 
       citation_count, cites_id, versions, cluster_id]"""
                                
    query = utils.get_user_input()
    
    params = {
        "engine": "google_scholar",
        "q": query,
        "api_key": "bd9ae4d322ca6af163e484036232d68bbfc7385d22eb5b3553fbdecb46509c20",
        "num": 20
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    organic_results = results['organic_results']

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

def serpapi_full_cite():
    """Scrapes Google scholar for full citations (Cite snippet)
       Iterates over a given df[result_id] and extracts full MLA citation
       Output is a dataframe with [full_citation] column"""
    df = serpapi_og_results()
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

def serpapi_cited_by_list(df):
    j = 0
    i = 0
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
            #print(f"Got citing papers from paper {j}")
            j = j + 1
            citing_papers.append(papers)
    flatList = [ item for elem in citing_papers for item in elem]
    citing_papers_df = pd.DataFrame(flatList)
    return citing_papers_df