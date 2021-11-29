#--------------------------------------------------------------------------#
#                 This code cleans the consolidated dataframe              # 
#--------------------------------------------------------------------------#
#                                 ---Usage---                              #
#               Call get_clean_df() on consolidated_df obtained from       #
#                 consolidated_df in data_collection module                #
#--------------------------------------------------------------------------#

from startupjh.utils import convert_to_datetime

import pandas as pd
import numpy as np

def clean_df(df):
    """Cleans the consolidated dataframe obtained with
       consolidated_df in data_collection module"""
    # Converts timestamp (str) to datetime
    df['published_date'] =  pd.to_datetime(df['published_date'], errors='coerce')
    # Converts list of authors to one single str of authors
    authors = []
    for index, row in df.iterrows():
        if type(row.authors) == list:
            str_authors = ", ".join(row.authors)
        else:
            str_authors = row.authors
        authors.append(str_authors)
    df['authors'] = authors
    # Converts list of key_words to tuple of kw
    key_words = []
    for index, row in df.iterrows():
        key_words.append(tuple(row.key_words))
    df['key_words'] = key_words
    # Drop duplicates if any
    df.drop_duplicates(inplace=True)
    # Replace missing values with 'no data'
    df['journal_is_oa'] = df.journal_is_oa.replace(['', np.nan], 'no data')
    df['published_date'] = df['published_date'].replace(np.datetime64('NaT'), 'no data')
    df['publisher'] = df.publisher.replace([None, np.nan], 'no data')
    return df