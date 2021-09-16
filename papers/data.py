# This code aims to collect data about scientific papers from Google Scholar API

import requests
import numpy as np
import pandas as pd
from serpapi import GoogleSearch
import re
from bs4 import BeautifulSoup

APIKEY = "e3ca696e087b4afc19a116f42f24b9aa"
BASE_URL = f"http://api.scraperapi.com?api_key={APIKEY}&url="

def get_key_words():
    topic_title = input("Enter key words: ")
    topic = topic_title.replace(" ", "+")
    return topic

def scraper_api(query):
    """Uses scraperAPI to scrape Google Scholar for 
    papers' Title, Year, Citations returns a dataframe"""
    #query = get_key_words()
    pages = np.arange(0,100,10)
    papers = []
    for page in pages:
        print(f"Scraping page {int(page/10) + 1}")
        webpage = f"https://scholar.google.com/scholar?start={page}&q={query}&hl=fr&as_sdt=0,5"
        url = BASE_URL + webpage
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        for paper in soup.find_all("div", class_="gs_ri"):
            title = paper.find("h3", class_="gs_rt").find("a").text
            if title == None:
                title = paper.find("h3", class_="gs_rt").find("span").text
            txt_year = paper.find("div", class_="gs_a").text
            year = re.findall('[0-9]{4}', txt_year)
            if year:
                year = list(map(int,year))[0]
            else:
                year = 0
            txt_cite = paper.find("div", class_="gs_fl").find_all("a")[2].string
            if txt_cite:
                citations = re.findall('[0-9]+', txt_cite)
                if citations:
                    citations = list(map(int,citations))[0]
                else:
                    citations = 0
            else:
                citations = 0
            papers.append({'title': title, 'year': year, 'citations': citations})
    papers_df = pd.DataFrame(papers)
    return papers_df

# automation+container+terminal

def serp_api(query):
    """Uses SerpAPI to request papers' Title, Year, Citations. Limited to 20 requests at a time..."""
    params = {
    "engine": "google_scholar",
    "q": query,
    "num": "15",
    "api_key": "bd9ae4d322ca6af163e484036232d68bbfc7385d22eb5b3553fbdecb46509c20"
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    organic_results = results['organic_results']

    papers = []
    for paper in organic_results:
        title = paper["title"]
        citations = paper["inline_links"]["cited_by"]["total"]
        pub_info = paper["publication_info"]["summary"]
        year = re.findall('[0-9]+', pub_info)
        year = list(map(int,year))[0]
        papers.append({'title': title, 'year': year, 'citations': citations})
    return papers