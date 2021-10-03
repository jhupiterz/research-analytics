# This code aims to collect data about scientific papers using Scraper API 
# https://www.scraperapi.com/
# Sometimes works sometimes not, without any error messages...

import requests
import numpy as np
import pandas as pd
import re
from bs4 import BeautifulSoup

APIKEY = "e3ca696e087b4afc19a116f42f24b9aa"
BASE_URL = f"http://api.scraperapi.com?api_key={APIKEY}&url="

def get_key_words():
    """get user input for topic to search"""
    topic_title = input("Enter key words: ")
    topic = topic_title.replace(" ", "+")
    return topic

def scraper_api(query, n_pages):
    """Uses scraperAPI to scrape Google Scholar for 
    papers' Title, Year, Citations, Cited By url returns a dataframe"""
    #query = get_key_words()
    pages = np.arange(0,(n_pages*10),10)
    papers = []
    for page in pages:
        print(f"Scraping page {int(page/10) + 1}")
        webpage = f"https://scholar.google.com/scholar?start={page}&q={query}&hl=fr&as_sdt=0,5"
        print(webpage)
        url = BASE_URL + webpage
        print(url)
        response = requests.get(url)
        print(response)
        soup = BeautifulSoup(response.content, "html.parser")
        #print(soup)

        for paper in soup.find_all("div", class_="gs_ri"):
            # get the title of each paper
            print(paper)
            title = paper.find("h3", class_="gs_rt").find("a").text
            if title == None:
                title = paper.find("h3", class_="gs_rt").find("span").text
            # get the year of publication of each paper
            txt_year = paper.find("div", class_="gs_a").text
            year = re.findall('[0-9]{4}', txt_year)
            if year:
                year = list(map(int,year))[0]
            else:
                year = 0
            # get number of citations for each paper
            txt_cite = paper.find("div", class_="gs_fl").find_all("a")[2].string
            if txt_cite:
                citations = re.findall('[0-9]+', txt_cite)
                if citations:
                    citations = list(map(int,citations))[0]
                else:
                    citations = 0
            else:
                citations = 0
            # get the "cited_by" url for later scraping of citing papers
            # had to extract the "href" tag and then reshuffle the url as not
            # following same pattern for pagination
            urls = paper.find("div", class_="gs_fl").find_all(href=True)
            if urls:
                for url in urls:
                    #print(url["href"])
                    if "cites" in url["href"]:
                        cited_url = url["href"]
                        index1 = cited_url.index("?")
                        url_slices = []
                        url_slices.append(cited_url[:index1+1])
                        url_slices.append(cited_url[index1+1:])

                        index_and = url_slices[1].index("&")
                        url_slices.append(url_slices[1][:index_and+1])
                        url_slices.append(url_slices[1][index_and+1:])
                        url_slices.append(url_slices[3][:23])
                        del url_slices[1]
                        new_url = "https://scholar.google.com.tw"+url_slices[0]+"start=00&hl=en&"+url_slices[3]+url_slices[1]+"scipsc="
            else:
                new_url = "no citations"
            print(title, year, citations, new_url)
            # appends everything in a list of dictionaries    
            papers.append({'title': title, 'year': year, 'citations': citations, 'cited_by_url': new_url})
    # converts the list of dict to a pandas df
    papers_df = pd.DataFrame(papers)
    papers_df.to_csv('papers.csv',index=False)
    return papers_df

def set_id(papers_df):
    """sets the tag number of each paper, works like a unique Id"""
    papers_df["tag"] = np.arange(1,len(papers_df)+1,1)
    return papers_df

def turn_page(url, page):
    """small function to turn pages in cited by url"""
    url_slices = []
    index_page = url.index("=")
    url_slices.append(url[:index_page+1])
    url_slices.append(page)
    url_slices.append(url[index_page+3:])
    new_url = url_slices[0]+url_slices[1]+url_slices[2]
    return new_url

def get_cited_by(papers_df):
    """sets the list of papers that cite each paper in papers_df
       each paper has a unique tag. cited_by data is a list of tags
       not working for now, problem with .text"""
    list_citing_papers = []
    for _, row in papers_df.iterrows():
        cited_url = row.cited_by_url
        citing_papers = []
        #pages = np.arange(0,50,10)
        for n_page in np.arange(1,5,1):
            url = BASE_URL + cited_url
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            for paper in soup.find_all("div", class_="gs_ri"):
                # get the title of each paper
                title = paper.find("h3", class_="gs_rt").find("a").text
                if title == None:
                    title = paper.find("h3", class_="gs_rt").find("span").text
                # get the year of publication of each paper
                txt_year = paper.find("div", class_="gs_a").text
                year = re.findall('[0-9]{4}', txt_year)
                if year:
                    year = list(map(int,year))[0]
                else:
                    year = 0
                # get number of citations for each paper
                txt_cite = paper.find("div", class_="gs_fl").find_all("a")[2].string
                if txt_cite:
                    citations = re.findall('[0-9]+', txt_cite)
                    if citations:
                        citations = list(map(int,citations))[0]
                    else:
                        citations = 0
                else:
                    citations = 0
                citing_papers.append({'title': title, 'year': year, 'citations': citations})
            cited_url = turn_page(cited_url, str(n_page*10))
        citing_papers_df = pd.DataFrame(citing_papers)
        list_citing_papers.append(citing_papers_df)
    papers_df["citing_papers"] = list_citing_papers
    return papers_df

def extract_keywords_from_title():
    pass