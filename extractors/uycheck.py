from requests import get
from bs4 import BeautifulSoup
from time import time
import pandas as pd
url = "http://uycheck.com/"
response = get(url)
soup = BeautifulSoup (response.text, "html.parser")
head = soup.findAll ('div', class_= 'bp-entry')
claims = []
date_publish = []
links = []
sources = []
"""
head_first = head [0]
title = (head_first.h2).text
link = (head_first.a)['href']
year_claim = (head_first.find('div', class_="bp-head").span.time).text
source = (head_first.find('div', class_="mom-post-meta").a).text
print (source)

are = soup.findAll('div', class_="main-col")[0]
b = are.find('a', class_='button medium full show-more-posts')['data-offset']
print (b)
"""

for container in head :

    # Claim
    claim = container.h2.text
    claims.append (claim) #on ajoute la claim

    #link
    link = (container.a)['href']
    links.append (link)

    #date de publication
    date = (container.find('div', class_="bp-head").span.time).text
    date_publish.append (date)

    #source de l'article
    source = (container.find('div', class_="mom-post-meta").a).text
    sources.append(source)


   #Affichage des Dataframe
test_df = pd.DataFrame({
       'claims' : claims,
       'links' : links,
       'date_publish' : date_publish,
       'source' : sources
   })
#print (len(head))
print (test_df)
test_df.to_csv("claims_uycheck.csv", sep=";")