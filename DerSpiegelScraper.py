# -*- coding: utf-8 -*-
"""
Created on Sun May 10 09:35:53 2020

@author: Amr.Khalil
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import os

category = ['politik', 'ausland','panorama', 'sport', 'wirtschaft', 'netzwelt', 'wissenschaft', 'kultur', 'geschichte']

my_dict={}

MAX_PAGES = 501

article_num = 1
for cat in category:
    for page in tqdm(range(1,MAX_PAGES),  desc='{:>15}'.format(cat)): 
        url = "https://www.spiegel.de/{}/p{}".format(cat, page)
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')

        articles = soup.select('article')
        for a in articles:
            my_dict[article_num]={"title":a.get('aria-label')}
            my_dict[article_num].update({"summary":"".join([x.text.strip()
                                                            for x in a.select('.leading-loose')])
                                        })
            my_dict[article_num].update({"date":"".join([x.text.strip()
                                                            for x in a.select('footer')])
                                        })
            my_dict[article_num].update({"categoty":cat})
            article_num +=1

if 'data' not in os.listdir():          
    !mkdir data
    df = pd.DataFrame.from_dict(data=my_dict, orient='index')
    df.to_csv('data/DerSpiegel.csv', index=False)
