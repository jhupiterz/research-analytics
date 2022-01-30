

import pandas as pd
import utils
from string import digits
import re

from collections import Counter


def get_most_common_key_words(df):
    """Sorts the key words of all papers in df according to their occurence.
       Input: df that MUST contain a "key_word" column
       Outpu: a new df with "key_word" and "occurence" columns """
    list_key_words = []
    for _, row in df.iterrows():
        for word in row.key_words:
            list_key_words.append(word)
    key_words_sorted = Counter(list_key_words).most_common()
    key_words_sorted_df = pd.DataFrame(key_words_sorted, columns=["key_word", "occurence"])
    index_names_kw = key_words_sorted_df[(key_words_sorted_df['key_word'] == "container") | (key_words_sorted_df['key_word'] == "automation") | (key_words_sorted_df['key_word'] == "terminal")].index
    key_words_sorted_df.drop(axis = 0, index = index_names_kw, inplace = True)
    return key_words_sorted_df

def get_most_active_author(df):
    # Separates authors from authors list for each paper
    authors_list = []
    for _, row in df.iterrows():
        authors_list.append(row.authors.split(","))
    # Flatten the list
    flat_authors_list = utils.flatten_list(authors_list)
    # Strip authors from blank spaces
    stripped_list = list(map(str.strip, flat_authors_list))
    # Remove "et al." from list
    words_to_remove = ["et al.", "and "]
    result = filter(lambda val: val != words_to_remove[0], stripped_list)
    list_authors = list(result)
    # Remove "and" from authors
    final_author_list = [i.strip("and ") for i in list_authors]
    # Count each author occurence and store in dataframe
    authors_sorted = Counter(final_author_list).most_common()
    authors_sorted_df = pd.DataFrame(authors_sorted, columns=["author", "occurence"])
    
    return authors_sorted_df

def get_most_active_journal(df):
    pub_info_list = df.pub_info
    # Get rid of any pub_info that is NOT a STR or that doesn't start with a letter
    indices_to_remove = []
    for index, e in pub_info_list.iteritems():
        if type(e) == str:
            if bool(re.match(r'\w', e)) != True:
                indices_to_remove.append(index)
            elif len(e) == 0:
                indices_to_remove.append(index)
        else:
            indices_to_remove.append(index)
    for i in indices_to_remove:
        del pub_info_list[i]
    # Get rid of the year and any thing after it
    list_journals = []
    for _, e in pub_info_list.iteritems():
        list_journals.append(re.split(r'\(\d{4}\)', e)[0])
    # Splitting by "." if any
    journals = []
    for e in list_journals:
        journals.append(re.split(r'\.', e)[0])
    # Get rid of all ENDING digits if any
    for i in range(len(journals)):
        #if bool(re.match(r'.+\d', e)):
        journals[i] = journals[i].strip().rstrip(digits).strip()
    # Sort journals by occurence and store in dataframe
    journals_sorted = Counter(journals).most_common()
    journals_sorted_df = pd.DataFrame(journals_sorted, columns=["journal", "occurence"])
    return journals_sorted_df