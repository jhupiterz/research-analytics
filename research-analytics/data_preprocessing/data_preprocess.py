#--------------------------------------------------------------------------#
#           This code preprocesses the data collected fom the API          # 
#--------------------------------------------------------------------------#

# imports ------------------------------------------------------------------
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import utils
import timeit
import re
import string

# function definitions ------------------------------------------------------
def extract_key_words(df):
    """what it does: extracts key words from paper titles
       argument: takes a dataframe as argument
       returns: the same dataframe with an extra 'key_words' column
       Attention: the df parameter MUST have a ["title"] column"""
    start = timeit.default_timer()
    
    key_words = []
    for i in range(len(df)):
        text = df['title'][i]
        text = text.lower()
        text = text.translate(str.maketrans('','',string.punctuation))
        text_tokens = word_tokenize(text)
        tokens_without_sw = [word for word in text_tokens if not word in stopwords.words()]
        key_words.append(tokens_without_sw)
    df['key_words'] = key_words
    return df

def extract_pub_info(df):
    """what it does: extracts author(s), year, and pub_info from full_citation
       arguments: takes a df as argument
       returns: the same df with 'authors', 'pub_info', 'year' columns
       Attention: df should have a 'title' column"""
    authors = []
    pub_info = []
    year = []

    for i, row in df.iterrows():
        find_year = re.search(r'[12]\d{3}', row.full_citation)
        if find_year:
            year.append(find_year.group(0))
        else: 
            year.append("no data")
        if '"' not in row.full_citation:
            split_str = row.full_citation.split('.')
        else:
            split_str = row.full_citation.split('"')
        authors.append(split_str[0].rstrip())
        pub_info.append(split_str[2].lstrip())
    df["authors"] = authors
    authors_list = utils.clean_google_authors(df)
    df["authors"] = authors_list
    df["pub_info"] = pub_info
    df["year"] = year
    return df