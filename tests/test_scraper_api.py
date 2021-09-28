from code.data import scraper_api
import pandas as pd

def test_scraper_api():
    assert len(scraper_api("biology+insects+molecular").columns) == 4