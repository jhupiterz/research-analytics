import numpy as np
import pandas as pd
from research_analytics.data_preprocessing import data_preprocess

def test_extract_key_words_on_normal_argument():
    """what it does: extracts key words from paper titles
       argument: takes a dataframe as argument
       returns: the same dataframe with an extra 'key_words' column
       Attention: the df parameter MUST have a ["title"] column"""
    df = pd.DataFrame({"title": ["This is an academic paper test", "This is another academic paper test"]})
    assert type(df) == pd.DataFrame
    assert "title" in df.columns
    df_expected = data_preprocess.extract_key_words(df)
    assert "key_words" in df_expected.columns

def test_extract_key_words_on_wrong_argument_type():
    """what it does: extracts key words from paper titles
       argument: takes a dataframe as argument
       returns: the same dataframe with an extra 'key_words' column
       Attention: the df parameter MUST have a ["title"] column"""
    df = np.array([["This is an academic paper test"], ["This is another academic paper test"]])
    assert (type(df) == pd.DataFrame) == False

def test_extract_key_words_on_wrong_df_format():
    """what it does: extracts key words from paper titles
       argument: takes a dataframe as argument
       returns: the same dataframe with an extra 'key_words' column
       Attention: the df parameter MUST have a ["title"] column"""
    df = pd.DataFrame({"authors": ["This is an academic author test", "This is another academic author test"]})
    assert type(df) == pd.DataFrame
    assert ("title" in df.columns) == False

def test_filter_data_by_time():
    start = int(1940)
    end = int(1990)
    df = pd.DataFrame({"year": [1918, 1923, 1948, 1978, 1989]})
    df_expected = data_preprocess.filter_data_by_time(df, [start, end])
    assert df_expected.shape == (3, 1)

def test_get_self_citation_ratios():
    author_id = "1741101"
    citation_expected = data_preprocess.get_self_citation_ratios(author_id, test=True)
    assert len(citation_expected) == 3
    assert citation_expected[2] > 15