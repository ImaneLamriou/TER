import bs4 as bs
import requests
import os
import re
import sys
import json

# os.system("clear")
# print(os.getcwd())

# test
def linksOfpagellapolitica():
    url = 'https://pagellapolitica.it/'
    uri = 'dichiarazioni/verificato?page='
    # for i in range(sys.maxsize):
    newArticles = {}
    # maxsize : c'est pour prendre toutes les pages depuis 2012
    totalNumberOfArticles = 1
    for i in range(sys.maxsize):
        pageNumber = i
        pageNumber = str(pageNumber)
        address = url + uri + pageNumber

        # si la resp est=200(pas d'erreur) on passe au if
        resp = requests.get(address)
        if resp:
            source = requests.get(address).text
            soup = bs.BeautifulSoup(source, "lxml")
            tables = soup.findAll('div', {'class': 'col-lg-3 mb-7'})

            """dans ce cas on récupere les titres et les liens avec le 'Href' chaque page a ça classe d'ou les differents If """

            for table in tables:

                if table.find('div', {'class': 'mb-0 px-2 min-height-title'}):
                    div = table.find(
                        'div', {'class': 'mb-0 px-2 min-height-title'})
                    title = div.find('span', {'class': 'h6'}).text.strip()
                elif table.find('div', {'class': 'mb-2 mt-2 px-2'}):
                    div = table.find('div', {'class': 'mb-2 mt-2 px-2'})

                    if div.find('span', {'class': 'h2'}):
                        # strip() pour enlever les espaces au début et fin de string
                        title = div.find('span', {'class': 'h2'}).text.strip()
                elif table.find('article', {'class': 'article'}):
                    article = table.find('article', {'class': 'article'})
                    p = article.find('p', {'class': 'font-size-15'})
                    if p.find('span', {'class': 'text-dark'}):
                        title = p.find(
                            'span', {'class': 'text-dark'}).text.strip()

                link = table.find('a', {'class': 'statement-link'})['href']
                # re : pour recupération des id de chaque page qu'il y'a entre le URI et le URL
                idPattern = re.search(r'/([0-9]+)/', link)
                idNumber = idPattern.group(1)
                newArticles[idNumber] = {'link': link,
                                         'title': title
                                         }
                print(totalNumberOfArticles, idNumber, title)
                totalNumberOfArticles += 1
                # le if ici c'est pour arreter la boucle car elle tourne indefiniment méme si l'ID n'existe pas
                if idNumber == str(96):
                    break
        if idNumber == str(96):
            break

    return newArticles

# creatio, d'un fichier JSON pour stocker tout les pages recupéréer (titre et links)


def writeLinksJson():
    file = 'dataBase/newArticlesLinks.json'
    newArticles = linksOfpagellapolitica()
    with open(file, 'w') as jsonOut:
        json.dump(newArticles, jsonOut, indent=2, ensure_ascii=False)
        # ensure_ascii=False : pour bien afficher les caractéres accentueux


writeLinksJson()

# pour lire le contenue de JSON


def readLinksJson():
    file = 'dataBase/newArticlesLinks.json'
    with open(file) as jsonIn:
        json.load(jsonIn)
