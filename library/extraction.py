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
    uriPage = 'dichiarazioni/verificato?page='
    articles = {}
    totalNumberOfArticles = 1
    for i in range(sys.maxsize):
        pageNumber = i
        pageNumber = str(pageNumber)
        address = url + uriPage + pageNumber

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
                    shortTitle = div.find('span', {'class': 'h6'}).text.strip()
                    guillemetPattern = re.search(r'\\', shortTitle)
                    print("guillemetPattern:",guillemetPattern)

                    if guillemetPattern:
                        shortTitle = shortTitle[2:]
                        print("guillemetPattern:",guillemetPattern)

                elif table.find('div', {'class': 'mb-2 mt-2 px-2'}):
                    div = table.find('div', {'class': 'mb-2 mt-2 px-2'})
                    if div.find('span', {'class': 'h2'}):
                        shortTitle = div.find('span', {'class': 'h2'}).text.strip()
                        guillemetPattern = re.search(r'\\', shortTitle)
                        if guillemetPattern:
                            shortTitle = shortTitle[2:]
                            print("guillemetPattern:",guillemetPattern)

                elif table.find('article', {'class': 'article'}):
                    article = table.find('article', {'class': 'article'})
                    p = article.find('p', {'class': 'font-size-15'})
                    if p.find('span', {'class': 'text-dark'}):
                        shortTitle = p.find(
                            'span', {'class': 'text-dark'}).text.strip()
                        guillemetPattern = re.search(r'\\', shortTitle)
                        if guillemetPattern:
                            shortTitle = shortTitle[2:]
                            print("guillemetPattern:",guillemetPattern)


                uriArticleID = table.find('a', {'class': 'statement-link'})['href']
                idPattern = re.search(r'/([0-9]+)/', uriArticleID)
                idNumber = idPattern.group(1)
                articles[idNumber] = {
                    'uriArticleID': uriArticleID,
                    'shortTitle': shortTitle
                }
                print(totalNumberOfArticles, idNumber, shortTitle)
                totalNumberOfArticles += 1

                if idNumber == str(215):
                    break
        if idNumber == str(215):
            break

    return articles, totalNumberOfArticles


def articleLinkIdGenerator():
    url = 'https://pagellapolitica.it/'
    uriPage = 'dichiarazioni/verificato?page='
    for i in range(sys.maxsize):
        pageNumber = i
        pageNumber = str(pageNumber)
        pageAddress = url + uriPage + pageNumber

        resp = requests.get(pageAddress)
        if resp:
            source = requests.get(pageAddress).text
            soup = bs.BeautifulSoup(source, "lxml")
            tables = soup.findAll('div', {'class': 'col-lg-3 mb-7'})
            for table in tables:
                uriArticleID = table.find('a', {'class': 'statement-link'})['href']
                idPattern = re.search(r'/([0-9]+)/', uriArticleID)
                idNumber = idPattern.group(1)
                articles[idNumber] = {
                    'url': uriArticleID,
                }
            if idNumber == str(215):
                break
        if idNumber == str(215):
            break
    return articles



def writeLinksJson():
    file = 'dataBase/articles.json'
    articles, totalNumberOfArticles = linksOfpagellapolitica()
    with open(file, 'w') as jsonOut:
        json.dump(articles, jsonOut, indent=2, ensure_ascii=False)


def readLinksJson():
    file = 'dataBase/articles.json'
    if os.path.isfile(file):
        with open(file) as jsonIn:
            data = json.load(jsonIn)
            return data
    else:
        print("I can't find ",file)
        


# def readLinksJson(**kwargs):
#     file = 'dataBase/newArticlesLinks.json'
#     with open(file) as jsonIn:
#         data = json.load(jsonIn)
#         for parameter in kwargs:

#     return data


# pour l'ajout d'un element dans un dictionnaire exsitant ,**dic[2] recupére
# tout les anciens elements du dic
# dic[2] = {**dic[2], "class": "21254465"}



def extractInfoArticle(id, online=False):

    article = {}
    if online:
        url = 'https://pagellapolitica.it/'
        uriArticle = 'dichiarazioni/'
        address = url + uriArticle + id
        resp = requests.get(address)
        if resp:
            source = requests.get(address).text
            soup = bs.BeautifulSoup(source, "lxml")
            
            #auteur
            p = soup.find('p', {'class': 'h4 mb-1 px-2 text-dark font-weight-light'})
            author = p.find('a', {'class': 'u-link-muted'}).text.strip()

            #le titre au complet quand on rentre dans l'article
            divFullBody = soup.find('div', {'class': 'col-lg-9 mb-9 mb-lg-0'})
            if divFullBody:
                divTitle = divFullBody.find('div', {'class': 'mb-2 mt-2 px-2'})
                if divTitle:
                    fullTitle = divTitle.find('span', {'class': 'h2'}).text.strip()
                else:
                    # dans les anciens artictles le fullText n'existe pas donc 
                    # si il ne le trouve pas il affiche le msg 
                    fullTitle = "No fullTitle"

            #les claims
            pclaimPX3 = soup.find('p', {'class': 'lead px-3 py-3 bg-light g-brd-around g-brd-lightblue'})
            pclaimPX2 = soup.find('p', {'class': 'h2 px-2'})
            if pclaimPX3:
                claim = pclaimPX3.text.strip()
            elif pclaimPX2:
                claim = pclaimPX2.find('span', {'class': 'text-darker'}).text.strip()
            
            #les dates(publication,origine) elles sont dans la méme classe d'ou l'utilisation
            #de divDates[0] pour la publication et divDates[1] pour l'origine
            divDate = soup.find('div', {'class': 'card-body pt-0 px-2'})
            divDates = divDate.findAll('div', {'class': 'col-lg-2 text-left'})
            datePublished = divDates[0].find('span', {'class': 'text-dark'}).text.strip()
            dateOrigin = divDates[1].find('span', {'class': 'text-dark'}).text.strip()

            #statement source
            divReferredLinks = divDate.find('div', {'class': 'col-lg-4'})
            statementSource = divReferredLinks.find('a', {'class': 'u-link-muted'})['href']

            #le join est pour concaténé les textes des balises P pour les mettre en un seul txt
            divMainArticle = soup.find('div', {'id': 'analisi-content'})
            listOfPInMainArticle = divMainArticle.findAll('p')
            mainText = [text.text.strip() for text in listOfPInMainArticle]
            mainArticle = ' '.join(mainText)

            #les liens de reference dans le main text
            listOfAllLinks = divMainArticle.findAll('a')
            listOfAllLinksHref = [link['href'] for link in divMainArticle.findAll('a')]
            
    else:
        data = readLinksJson()
        # pour l'ajout d'un element dans un dictionnaire exsitant ,**dic[2] recupére
        # tout les anciens elements du dic
        data[id] = {
                    **data[id], 
                    "source":url,                           # le site de fact checking
                    "claim":claim,
                    "body":mainArticle,                     # le text de l'article
                    "referred_links":listOfAllLinksHref,    # tous les liens dans le texte
                    "title":fullTitle,                      # le titre de l'article
                    "date":dateOrigin,                      # date de la claim
                    "url": address,                         #url de l'article
                    "tags":"tags",                          # les mots cles
                    "author": author,                       # auteur de la claim
                    "datePublished":datePublished,
                    "rating_value":"rating_value",          # la valeur de la veracite
                    "statementSource":statementSource,
                    "claim_entities":"claim_entities",      # les entities nomes qui est extraite de la claim
                    "body_entities":"body_entities",        # les entities nomes qui est extraite de l'article
                    "keyword_entities":"keyword_entities",  # parmi les tages, les entities nomes a partir de la tag
                    "author_entities":"author_entities",    # les entities nomes a partir de l'auteur de la claim
                    "review_author":"review_author"         # l'auteur de l'article
                    
                    }




    
    article = {
        id: {
            "source":url,                           # le site de fact checking
            "claim":claim,
            "body":mainArticle,                     # le text de l'article
            "referred_links":listOfAllLinksHref,    # tous les liens dans le texte
            "title":fullTitle,                      # le titre de l'article
            "date":dateOrigin,                      # date de la claim
            "url": address,                         #url de l'article
            "tags":"tags",                          # les mots cles
            "author": author,                       # auteur de la claim
            "datePublished":datePublished,
            "rating_value":"rating_value",          # la valeur de la veracite
            "statementSource":statementSource,
            "claim_entities":"claim_entities",      # les entities nomes qui est extraite de la claim
            "body_entities":"body_entities",        # les entities nomes qui est extraite de l'article
            "keyword_entities":"keyword_entities",  # parmi les tages, les entities nomes a partir de la tag
            "author_entities":"author_entities",    # les entities nomes a partir de l'auteur de la claim
            "review_author":"review_author"         # l'auteur de l'article
            
        }
    }
    

    return article


