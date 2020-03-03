#!/home/e20190009681/myGitProjects/S2/TER/TER/env/bin/python

import bs4 as bs
import requests
import os
import re
import sys
import json
import extraction as ter

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


a = ter.articleLinkIdGenerator()

for id in a.keys():
    article = ter.extractInfoArticle(id)
    print("article: ", article)
