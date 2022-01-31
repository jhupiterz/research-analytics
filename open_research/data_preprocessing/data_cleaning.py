#--------------------------------------------------------------------------#
#                 This code cleans the consolidated dataframe              # 
#--------------------------------------------------------------------------#

# imports ------------------------------------------------------------------
import pandas as pd
import numpy as np

# function definitions -----------------------------------------------------
def clean_df(df):
    """what it does: cleans the consolidated dataframe
       arguments: takes a dataframe as argument
       returns: the cleaned dataframe"""

    df['published_date'] =  pd.to_datetime(df['published_date'], errors='coerce')
    
    # Convert list of authors to one single str of authors
    authors = []
    for index, row in df.iterrows():
        if type(row.authors) == list:
            str_authors = ", ".join(row.authors)
        else:
            str_authors = row.authors
        authors.append(str_authors)
    df['authors'] = authors
    df['authors'] = df['authors'].str.lstrip()
    
    # Convert list of key_words to tuple of kw
    key_words = []
    for index, row in df.iterrows():
        key_words.append(tuple(row.key_words))
    df['key_words'] = key_words
    
    # basic cleaning
    df.drop_duplicates(inplace=True)
    df['authors'] = df.authors.str.split(', ')
    df['journal_is_oa'] = df.journal_is_oa.replace(['', np.nan], 'no data')
    df['publisher'] = df.publisher.replace([None, np.nan], 'no data')
    df['published_date'] =  pd.to_datetime(df['published_date'], errors='coerce')
    df['published_year'] = pd.DatetimeIndex(df['published_date']).year
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