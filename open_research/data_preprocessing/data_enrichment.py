#--------------------------------------------------------------------------#
#                 This code gets the citation count for papers             #
#--------------------------------------------------------------------------#

# imports ------------------------------------------------------------------
from serpapi import GoogleSearch
import pandas as pd
import numpy as np

# function definitions ------------------------------------------------------
def get_citation_count(consolidated_df):
    """what it does: queries SerpAPI for the citation count for each paper in consolidated_df
       arguments: takes a dataframe as argument (should be consolidated_df)
       returns: the condolidated_df including a 'citation_coun' column"""
    
    # iterates on df to query and retrieve citation_count
    citation_count = []
    for index, row in consolidated_df.iterrows():
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
    consolidated_df['citation_count'] = citation_count
    return consolidated_df