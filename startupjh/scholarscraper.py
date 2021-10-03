# This code aims to collect data about scientific papers without using any APIs
# only using web scraping

import requests
import numpy as np
import pandas as pd
import re
from bs4 import BeautifulSoup

def scraper_api(query, n_pages):
    """Scraes Google Scholar web pages for 
    papers' Title, Year, Citations, Cited By url returns a dataframe"""
    #query = get_key_words()
    pages = np.arange(0,(n_pages*10),10)
    papers = []
    for page in pages:
        print(f"Scraping page {int(page/10) + 1}")
        url = f"https://scholar.google.com/scholar?start={page}&q={query}&hl=fr&as_sdt=0,5"
        print(url)
        response = requests.get(url)
        print(response)
        soup = BeautifulSoup(response.content, "html.parser")

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