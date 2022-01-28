#--------------------------------------------------------------------------#
#                 This code gets the citation count for papers             #
#             in consolidated_df obtained in data_collection module        # 
#--------------------------------------------------------------------------#
#                               ---Usage---                                #
#         Call get_citation_count() on consolidated_df obtained from       #
#                 consolidated_df in data_collection module                #
#--------------------------------------------------------------------------#

from serpapi import GoogleSearch
import pandas as pd
import numpy as np

def get_citation_count(df):
    """Queries SerpAPI for Google Scholar results and only returns 
       the citation count for each paper in df.
       df should be consolidated df obtained from data_collection module"""
    citation_count = []
    for index, row in df.iterrows():
        if pd.notna(row.citation_count):
            citations = row.citation_count
        else:
            query = row.title + " " + str(' '.join(row.authors))

            params = {
                    "engine": "google_scholar",
                    "q": query,
                    "api_key": "bd9ae4d322ca6af163e484036232d68bbfc7385d22eb5b3553fbdecb46509c20",
                    "num": 1
                }

            search = GoogleSearch(params)
            results = search.get_dict()
            if 'organic_results' in results:
                organic_results = results['organic_results']

                if "inline_links" in organic_results[0]:
                    if "cited_by" in organic_results[0]["inline_links"]:
                        citations = organic_results[0]["inline_links"]["cited_by"]["total"]
                    else: 
                        citations = 0
            else:
                citations = np.nan
        citation_count.append(citations)
    df['citation_count'] = citation_count
    return df