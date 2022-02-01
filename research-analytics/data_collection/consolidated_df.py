#--------------------------------------------------------------------------#
#    consolidates, cleans, enriches data scraped from the different APIs   #
#--------------------------------------------------------------------------#

# imports ------------------------------------------------------------------
import pandas as pd
from data_preprocessing import data_cleaning, data_enrichment
from utils import format_user_input, get_user_input
from data_collection import core_api, doaj_api, google_api, unpaywall_api

# function definitions -----------------------------------------------------
def get_consolidated_df():
    """what it does: consolidates all data from DOAJ, CORE, Unpaywall,
                     and GoogleScholar APIs into a single dataframe
       arguments: no arguments
       returns: the consolidated dataframe and the input query"""
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
    """what it does: cleans and enriches the consolidated df
       arguments: no arguments
       returns: the cleaned and enriched df and the input query"""
    df, query_keywords = get_consolidated_df()
    query = tuple(query_keywords.split())
    df = data_cleaning.clean_df(df)
    df = data_enrichment.get_citation_count(df)
    df['authors'] = data_cleaning.clean_authors_list(df)
    return df, query


