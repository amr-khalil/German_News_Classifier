# -*- coding: utf-8 -*-
"""
Created on Sun May 10 09:35:53 2020

@author: Amr.Khalil
"""
# Import libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import os

# The website categories
category = ['politik', 'ausland','panorama', 'sport', 'wirtschaft', 'netzwelt', 'wissenschaft', 'kultur', 'geschichte']
# Create a dictionary for articles
my_dict={}
# Number of pages that will be scraped for every categotry
MAX_PAGES = 501
# Indexing the articles
article_num = 1

for cat in category:
    for page in tqdm(range(1,MAX_PAGES),  desc='{:>15}'.format(cat)): 
        url = "https://www.spiegel.de/{}/p{}".format(cat, page)
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')

        articles = soup.select('article') # select all articles
        for a in articles:
            # Select the articles' titles from attribute 'aria-label'
            my_dict[article_num]={"title":a.get('aria-label')}
            
            # Select the articles' summary from class 'leading-loose'
            my_dict[article_num].update({"summary":"".join([x.text.strip()
                                                            for x in a.select('.leading-loose')])
                                        })
            # Select the articles' date from 'footer'
            my_dict[article_num].update({"date":"".join([x.text.strip()
                                                            for x in a.select('footer')])
                                        })
            # Add the category
            my_dict[article_num].update({"categoty":cat})
            
            # index' Increment  
            article_num +=1

if 'data' not in os.listdir():          
    # Create a folder
    !mkdir data
    #Convert my_dict to DataFrame
    df = pd.DataFrame.from_dict(data=my_dict, orient='index')
    # Drop duplicate articles
    df2 = df.drop_duplicates(subset='title', keep='first')
    # Save as csv as utf-16 due to spicial German charachters
    df2.to_csv('data/DerSpiegel.csv', index=False, encoding = 'utf-16')
