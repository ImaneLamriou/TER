#!/home/e20190009681/myGitProjects/S2/TER/TER/env/bin/python

import bs4 as bs
import requests
import os
import re
import sys
import json
import library.extraction as ter


# Vero = 1
# C'eri quasi = 2
# Ni = 3
# Pinocchio andante = 4
# Panzana pazzesca = 5


# affichage des info extraites qu'on  recupere dans JSON
# inp = sys.argv
# id = inp[1]
# data = ter.readLinksJson()
# if len(inp) != 2:
#     print("Hey, What are you doing?")
# elif len(inp) == 2 and data[id]:
#     # le \t c'est pour l'espace durant l'affichag
#     print(ter.extractInfoArticle(id, online=True))

# afficher tous les articles
# afficher plusieur articles

# for i,id,links in enumerate(ter.articleLinkIdGenerator()):
#     print("id"+i,"= ",id,"\n",links)

# ter.writeLinksJson()


# pageLinks = ter.pageLinks("1")
# link = pageLinks[0]


# lastArticle = ter.extractInfoArticle("1269", online=True)
# print(lastArticle)


for pageNumber in range(1, 174):
    pageLinks = ter.pageLinks(str(pageNumber))
    print("Page number:", pageNumber)
    for page in pageLinks:
        id = ter.idNumber(page)
        lastArticle = ter.extractInfoArticle(id, online=True)
        ter.writeLinksJson(lastArticle, append=True)
        print('rating_value = ', lastArticle[id]["rating_value"])
        print("\n")

# ter.findPageNumberOfID("8436")

# print(ter.pageLinks("7"))
