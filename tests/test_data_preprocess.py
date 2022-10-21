import pytest
import numpy as np
import pandas as pd
import utils
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

def test_extract_pub_info():
    """what it does: extracts author(s), year, and pub_info from full_citation
       arguments: takes a df as argument
       returns: the same df with 'authors', 'pub_info', 'year' columns
       Attention: df should have a 'full_citation' column"""
    df = pd.DataFrame({"full_citation": ["George and . Teece . 2020"]})
    assert type(df) == pd.DataFrame
    assert "full_citation" in df.columns
    df_expected = data_preprocess.extract_pub_info(df)
    assert "authors" in df_expected.columns
    assert "pub_info" in df_expected.columns
    assert "year" in df_expected.columns