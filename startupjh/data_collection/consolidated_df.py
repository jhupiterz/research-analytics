#--------------------------------------------------------------------------#
#        This code consolidates data scraped from the different APIs       #
#--------------------------------------------------------------------------#
#                                 ---Usage---                              #
#          Just run the method consolidated_df() and it will ask for       #
#                   your search query and return a df populated            #
#                      with results from 4 different APIs                  #
#--------------------------------------------------------------------------#

import pandas as pd

from startupjh.data_collection import semantic_api
from startupjh.data_preprocessing import data_cleaning, data_enrichment

from startupjh.utils import format_user_input, get_user_input
from startupjh.data_collection import core_api, doaj_api, google_api, unpaywall_api

def get_consolidated_df():
    """for other APIs (DOAJ, CORE, Unpaywall, GoogleScholar"""
    query = get_user_input()
    search_query = format_user_input(query)

    df_unpaywall = unpaywall_api.unpaywall_api(search_query)
    df_doaj = doaj_api.doaj_api(search_query)
    df_core = core_api.core_api(search_query)
    df_google = google_api.serpapi_full_cite(search_query)

    consolidated_df = pd.concat([df_unpaywall, df_doaj, df_core, df_google]).reset_index(drop=True)
    consolidated_df.drop(labels=['doi', 'affiliations', 'genre', 'is_oa', 'link', 'abstract', 'number_of_pages', 
                                'document_type', 'full_text', 'language', 'references', 
                                'snippet', 'cites_id', 'full_citation'], axis=1, inplace=True)
    
    return consolidated_df, query

def get_final_df():
    """for other APIs (DOAJ, CORE, Unpaywall, GoogleScholar"""
    df, query_keywords = get_consolidated_df()
    query = tuple(query_keywords.split())
    df = data_cleaning.clean_df(df)
    df = data_enrichment.get_citation_count(df)
    df['authors'] = data_cleaning.clean_authors_list(df)
    return df, query


