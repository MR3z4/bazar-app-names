#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 16:27:10 2018

@author: MohammadReza Mohammadzade
"""

import csv
import requests
from bs4 import BeautifulSoup
urls = ['https://cafebazaar.ir/cat/?l=en']
f = csv.writer(open('all-app-names.csv', 'w'))
f.writerow(['Names', 'Links','Category'])
for url in urls:
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    m_bod = soup.find(class_='col-md-6')
    cat_box = m_bod.find_all('a')
    
    c_urls = []
    for link in cat_box :
        c_urls.append('https://cafebazaar.ir'+link.get('href'))
for url in c_urls:
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    bod = soup.find(class_='container-body')
    more_box = bod.find_all(class_='msht-row-more pull-right')
    s_urls = []
    for i in range(0,len(list(more_box))) :
        link_box = more_box[i].find('a')
        if ((link_box.get('href').replace('\n','').lstrip().rstrip().find('best-new')!=-1) or (link_box.get('href').replace('\n','').lstrip().rstrip().find('top-rated')!=-1) or (link_box.get('href').replace('\n','').lstrip().rstrip().find('new-apps')!=-1)):
            continue
        s_urls.append('https://cafebazaar.ir'+link_box.get('href').replace('\n','').lstrip().rstrip())
    
    for url1 in s_urls:
        page = requests.get(url1)
        soup = BeautifulSoup(page.text, 'html.parser')
        cat = soup.find(class_='container-head')
        cat = str(cat.find('h1').contents[0]).lstrip().rstrip()
        app_box = soup.find(class_='row msht-app-list')
        app_l = app_box.find_all('a')
        app_sp = app_box.find_all(class_='msht-app-name')
        names = []
        links = []
        for app_link in app_l:
            links.append(app_link.get('href').replace('\n','').replace(' ','').replace('/app/','').replace('/?l=en',''))
        for i in range(0,len(list(app_sp))) :
            sp_cont = app_sp[i].find('span').contents[0]
            names.append(str(sp_cont).lstrip().rstrip().replace('\n','')) 
            f.writerow([names[i],links[i],cat])
        
