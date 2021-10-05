#--------------------------------------------------------------------------#
#           This code preprocesses the data collected fom the API          # 
#--------------------------------------------------------------------------#
#                                 ---Usage---                              #
# To get the primary results of a Google Scholar search run the following: #
#                   primaryResults = serpapi_full_cite()                   #
#      To get the papers citing the primary results run the following:     #
#            citing_papers = serpapi_cited_by_list(primaryResults)         #
#                                                                          #
#    N.B. the second command will only run if the first one has been run   #
#--------------------------------------------------------------------------#

import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
from nltk.tokenize import word_tokenize

import pandas as pd
import numpy as np
import re
import string

def extract_key_words(df):
    """method to extract key words from paper titles
       gets a dataframe parameter and returns the same 
       dataframe with an extra ["key_words"] column
       Attention: the df parameter MUST have a ["title"] column"""
    key_words = []
    for i in range(len(df)):
        text = df['title'][i]
        text = text.lower()
        text = text.translate(str.maketrans('','',string.punctuation))

        text_tokens = word_tokenize(text)

        tokens_without_sw = [word for word in text_tokens if not word in stopwords.words()]
        #filtered_sentence = (", ").join(tokens_without_sw)

        key_words.append(tokens_without_sw)
        
    df['key_words'] = key_words 
    
    return df

def extract_pub_info(primary_df):
    """Extracts author(s), year, and pub_info from full_citation
       for now primary_df MUST have a ["full_citation"] column
       only works for primaryResults - will be updated for citingPapers
       returns primary_df with three extra columns ["authors", "pub_info", "year"]"""
    authors = []
    pub_info = []
    year = []

    for _, row in primary_df.iterrows():
        split_str = row.full_citation.split('"')
        authors.append(split_str[0].rstrip())
        pub_info.append(split_str[2].lstrip())
        find_year = re.search(r'[12]\d{3}', split_str[2])
        year.append(find_year.group(0))
    primary_df["authors"] = authors
    primary_df["pub_info"] = pub_info
    primary_df["year"] = year
    
    return primary_df