import bs4 as bs
import requests
import os
import re
import sys
import json

def linksOfAfricacheckFr():
    url = 'https://fr.africacheck.org/'
    uriPage = 'dichiarazioni/verificato?page='
    # maxsize : c'est pour prendre toutes les pages depuis 2012
    articles = {}
    totalNumberOfArticles = 1
    for i in range(sys.maxsize):
        pageNumber = i
        pageNumber = str(pageNumber)
        address = url + uriPage + pageNumber

        # si la resp est=200(pas d'erreur) on passe au if
        resp = requests.get(address)
        if resp:
            source = requests.get(address).text
            soup = bs.BeautifulSoup(source, "lxml")
            tables = soup.findAll('div', {'class': 'secondary-article report nonlead'})