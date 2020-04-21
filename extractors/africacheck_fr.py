import bs4
import requests
import os
import re
import sys
import json
import pickle


def links(online=False):
    pickleLinks = "links.pickle"
    url = 'https://fr.africacheck.org/articles/page/'

    # maxsize : c'est pour prendre toutes les pages depuis nov 2012
    links = []
    totalNumberOfArticles = 1
    if online:
        i = 1
        while True:
            pageNumber = i
            pageNumber = str(pageNumber)
            address = url + pageNumber

            # si la resp est=200(pas d'erreur) on passe au if  request= juste pour connaitre la reponse
            resp = requests.get(address)
            source = requests.get(address).text
            soup = bs4.BeautifulSoup(source, "lxml")
            nextPage = soup.find('a', {'class': 'next page-numbers'})
            # on recupere le code source de page dans la variable source avec .text a la fin

            page = soup.find('div', {'id': 'content'})

            articles = page.findAll(
                'article', {'class': 'secondary-article report nonlead'})
            print("*"*40)
            print(pageNumber)
            for article in articles:
                link = article.find('a')['href']
                # ajouter les liens dans la liste 'liens'
                links.append(link)
                print("Article number: ", totalNumberOfArticles, link)
                totalNumberOfArticles += 1
            if not nextPage:
                break
            i += 1
        with open(pickleLinks, 'wb') as file:
            pickle.dump(links, file)
    else:
        with open(pickleLinks, 'rb') as file:
            links = pickle.load(file)
    return links


def beautifulObject(link):
    resp = requests.get(link)
    # on recupere le code source de page dans la variable source avec .text a la fin
    source = requests.get(link).text
    soup = bs4.BeautifulSoup(source, "lxml")
    div = soup.find('div', {'class': 'report-verdict'})
    if div:
        return soup
    else:
        return None


def title(soup):
    if soup:
        header = soup.find('header', {'class': 'article-header clearfix'})
        title = header.find('h1', {'class': 'single-title'}).text
    else:
        title = "No Title"
    return title


def claimAndSource(soup):
    if soup:
        div = soup.find('div', {'report-claim'})
        claimAndSource = div.findAll('p')
        claim = claimAndSource[0].text.strip()
        source = claimAndSource[1].text.strip()
        # re.sub(r'Affirmation', ' ', claim).strip()
    else:
        claim = "No Claim"
        source = "No Source"
    return claim, source


def veracity(soup):
    if soup:
        div = soup.find('div', {'class': 'report-verdict'})
        veracity = div.find('div', {'class': 'verdict-stamp'}).text
    else:
        veracity = "No Veracity"
    return veracity


def date(soup):
    if soup:
        div = soup.find('div', {'class': 'article-content'})
        date = div.find('time', {'pubdate datetime'})
    else:
        date = 'No Date'
    return date


def api():
    link = "https://fr.africacheck.org/wp-json/"
    resp = requests.get(link)
    source = requests.get(link).json()
    file = "api.json"
    with open(file, "w") as jsonFile:
        json.dump(source, jsonFile, indent=2)

    # premiere ligne de la fonction qui recupere les liens
links = links(online=False)
# https://fr.africacheck.org/reports/covid-19-le-margousier-neem-ne-contient-pas-de-la-chloroquine/
print("*"*100)

link = links[2]
print("Article link: \n", link)
soup = beautifulObject(link)
title = title(soup)
claim, source = claimAndSource(soup)
veracity = veracity(soup)

print("Number of articles:", len(links))
print("\nTitle:", title)
print("\nclaim:", claim, "\nSource:", source)
print("\nVeracity:", veracity)

api()
