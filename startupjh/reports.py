# Code to get the data from data.py and do some basic data visualization

from startupjh.data import scraper_api
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
import re
from bs4 import BeautifulSoup

def pub_per_year(topic):
    df = scraper_api(topic)
    #plt.figure(figsize=(300, 150))
    plt.subplot(1,2,1)
    plt.plot(df.groupby("year").count()["title"])
    plt.xlabel("Year")
    plt.ylabel("Number of publications")
    plt.title(f"Topic: {topic}")
    plt.xlim((1975,2025))
    plt.xticks(np.arange(1980,2025,5))

    plt.subplot(1,2,2)
    plt.bar(df.groupby("year").count()["title"].index, df.groupby("year").count()["title"])
    plt.xlabel("Year")
    plt.ylabel("Number of publications")
    plt.title(f"Topic: {topic}")
    plt.xlim((1980,2025))
    plt.xticks(np.arange(1980,2025,5))
    
    plt.show()