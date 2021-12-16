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
    df['authors'] = df['authors'].str.lstrip()
    # Converts list of key_words to tuple of kw
    key_words = []
    for index, row in df.iterrows():
        key_words.append(tuple(row.key_words))
    df['key_words'] = key_words
    # Drop duplicates if any
    df.drop_duplicates(inplace=True)
    # Once duplicates have been dropped, make a list out of authors again
    df['authors'] = df.authors.str.split(', ')
    # Replace missing values with 'no data'
    df['journal_is_oa'] = df.journal_is_oa.replace(['', np.nan], 'no data')
    df['published_date'] = df['published_date'].replace(np.datetime64('NaT'), 'no data')
    df['publisher'] = df.publisher.replace([None, np.nan], 'no data')
    # Convert date str into datetime
    df['published_date'] =  pd.to_datetime(df['published_date'], errors='coerce')
    # Extract year from datetime
    df['published_year'] = pd.DatetimeIndex(df['published_date']).year
    # Strip volume numbers from journal name
    df['journal_name'] = df['journal_name'].str.rstrip('1234567890.-').str.strip()
    return df

def clean_authors_list(df):
    cleaned_authors_list = []
    for element in df.authors:
        new_authors = []
        for author in element:
            if ' and ' in author:
                author = author.lstrip(' and ')
            new_authors.append(author)
        cleaned_authors_list.append(new_authors)
    return cleaned_authors_list