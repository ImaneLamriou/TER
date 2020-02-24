import bs4 as bs
import requests
import os
import re
import sys
import json

# os.system("clear")
# print(os.getcwd())


def linksOfpagellapolitica():
    url = 'https://pagellapolitica.it/'
    uri = 'dichiarazioni/verificato?page='
    # for i in range(sys.maxsize):
    newArticles = {}
    articleNumbers = 1
    for i in range(sys.maxsize):
        pageNumber = i
        pageNumber = str(pageNumber)
        address = url + uri + pageNumber

        resp = requests.get(address)

        if resp:
            source = requests.get(address).text
            soup = bs.BeautifulSoup(source, "lxml")
            tables = soup.findAll('div', {'class': 'col-lg-3 mb-7'})

            # dans ce cas on récupere les titres et les liens avec le 'Href'

            for table in tables:

                if table.find('div', {'class': 'mb-0 px-2 min-height-title'}):
                    div = table.find(
                        'div', {'class': 'mb-0 px-2 min-height-title'})
                    title = div.find('span', {'class': 'h6'}).text
                elif table.find('div', {'class': 'mb-2 mt-2 px-2'}):
                    div = table.find('div', {'class': 'mb-2 mt-2 px-2'})

                    if div.find('span', {'class': 'h2'}):
                        title = div.find('span', {'class': 'h2'}).text
                elif table.find('article', {'class': 'article'}):
                    article = table.find('article', {'class': 'article'})
                    p = article.find('p', {'class': 'font-size-15'})
                    if p.find('span', {'class': 'text-dark'}):
                        title = p.find(
                            'span', {'class': 'text-dark'}).text

                link = table.find('a', {'class': 'statement-link'})['href']
                idPattern = re.search(r'/([0-9]+)/', link)
                idNumber = idPattern.group(1)
                # print("Article\n = Link:", link, "\nTitle:", title)
                newArticles[idNumber] = {'link': link,
                                         'title': title
                                         }
                print(articleNumbers, idNumber, title)
                articleNumbers += 1

    return newArticles


def writeLinksJson():
    file = 'dataBase/newArticlesLinks.json'
    newArticles = linksOfpagellapolitica()
    with open(file, 'w') as jsonOut:
        json.dump(newArticles, jsonOut, indent=2)


# writeLinksJson()
def readLinksJson():
    file = 'dataBase/newArticlesLinks.json'
    with open(file) as jsonIn:
        json.load(jsonIn)


data = readLinksJson()
print(len(data))
