#--------------------------------------------------------------------------#
#           This code preprocesses the data collected fom the API          # 
#--------------------------------------------------------------------------#

# imports ------------------------------------------------------------------
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
nltk.download('punkt')
nltk.download('stopwords')
from research_analytics import utils
import requests
import re
import pandas as pd
import string

# function definitions ------------------------------------------------------
def extract_key_words(df):
    """what it does: extracts key words from paper titles
       argument: takes a dataframe as argument
       returns: the same dataframe with an extra 'key_words' column
       Attention: the df parameter MUST have a ["title"] column"""
    
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

def filter_data_by_time(dataframe, filter_values):
    start = int(filter_values[0])
    end = int(filter_values[1])
    dataframe = dataframe[(dataframe['year'] >= start) & (dataframe['year'] <= end)]
    return dataframe

def get_citations_for_one_paper(paper_id, test=False):
    if test == True:
        url_ref = f"https://api.semanticscholar.org/graph/v1/paper/{paper_id}/citations?fields=authors&limit=1"
    else:
        url_ref = f"https://api.semanticscholar.org/graph/v1/paper/{paper_id}/citations?fields=authors&limit=100"
    references = requests.get(url_ref).json()
    return references['data']

def get_papers_for_one_author(author_id, test=False):
    if test == True:
        url = f"https://api.semanticscholar.org/graph/v1/author/{author_id}?fields=name,paperCount,citationCount,hIndex,papers.referenceCount,papers.paperId,papers.citationCount&limit=1"
    else:
        url = f"https://api.semanticscholar.org/graph/v1/author/{author_id}?fields=name,paperCount,citationCount,hIndex,papers.referenceCount,papers.paperId,papers.citationCount"
    papers_by_author = requests.get(url).json()
    papers_df = pd.DataFrame(papers_by_author['papers']).sort_values("citationCount", ascending=False)
    papers_df = papers_df[papers_df['referenceCount'] != 0]
    if len(papers_df) >= 20:
        sample_papers_df = papers_df.sample(20)
    else:
        sample_papers_df = papers_df
    return sample_papers_df

def get_self_citation_ratios(author_id, test=False):
    self_citation = 0
    coauthor_citation = 0
    nonself_citation = 0
    test_df = get_papers_for_one_author(author_id, test)
    test_df.shape
    for _, row in test_df.iterrows():
        citations = get_citations_for_one_paper(row['paperId'], test)
        for citation in citations:
            authors = citation['citingPaper']['authors']
            author_list = [x['authorId'] for x in authors]
            if author_list:
                if author_list[0] == author_id:
                    self_citation = self_citation + 1
                elif author_id in author_list[1:]:
                    coauthor_citation = coauthor_citation + 1
                elif author_id not in author_list:
                    nonself_citation = nonself_citation + 1
    return [self_citation, coauthor_citation, nonself_citation]