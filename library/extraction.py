import bs4 as bs
import requests
import os
import re
import sys
import json
import library

# os.system("clear")
# print(os.getcwd())

# test


def common(a, b):
    c = [value for value in a if value in b]
    return c


def common2(a, b):
    return set(a).intersection(b)


def linksOfpagellapolitica():
    url = 'https://pagellapolitica.it/'
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
            tables = soup.findAll('div', {'class': 'col-lg-4 mb-7'})

            # dans ce cas on récupere les titres et les liens avec le 'Href' chaque page a ça classe d'ou les differents If

            for table in tables:
                if table.find('div', {'class': 'mb-0 px-2 min-height-title'}):
                    div = table.find(
                        'div', {'class': 'mb-0 px-2 min-height-title'})
                    shortTitle = div.find('span', {'class': 'h6'}).text.strip()
                    guillemetPattern = re.search(r'\\', shortTitle)

                    if guillemetPattern:
                        shortTitle = shortTitle[2:]

                # strip() pour enlever les espaces au début et fin de string
                elif table.find('div', {'class': 'mb-2 mt-2 px-2'}):
                    div = table.find('div', {'class': 'mb-2 mt-2 px-2'})
                    if div.find('span', {'class': 'h2'}):
                        shortTitle = div.find(
                            'span', {'class': 'h2'}).text.strip()
                        guillemetPattern = re.search(r'\\', shortTitle)
                        if guillemetPattern:
                            shortTitle = shortTitle[2:]

                elif table.find('article', {'class': 'article'}):
                    article = table.find('article', {'class': 'article'})
                    p = article.find('p', {'class': 'font-size-15'})
                    if p.find('span', {'class': 'text-dark'}):
                        shortTitle = p.find(
                            'span', {'class': 'text-dark'}).text.strip()
                        guillemetPattern = re.search(r'\\', shortTitle)
                        if guillemetPattern:
                            shortTitle = shortTitle[2:]

                # re : pour recupération des id de chaque page qu'il y'a entre le URI et le URL
                uriArticleID = table.find(
                    'a', {'class': 'statement-link'})['href']
                idPattern = re.search(r'/([0-9]+)/', uriArticleID)
                idNumber = idPattern.group(1)
                articles[idNumber] = {
                    'uriArticleID': uriArticleID,
                    'shortTitle': shortTitle
                }
                print(totalNumberOfArticles, idNumber, shortTitle)
                totalNumberOfArticles += 1

                # le if ici c'est pour arreter la boucle car elle tourne
                # indefiniment méme si l'ID n'existe pas
                if idNumber == str(215):
                    break
        if idNumber == str(215):
            break

    return articles, totalNumberOfArticles


def articleLinkIdGenerator(online=False):
    # on a utilisé le online=false car si on est pas en ligne on pourra
    # utiliser la dataBase pour afficher les resultats voulue
    url = 'https://pagellapolitica.it/'
    uriPage = 'dichiarazioni/verificato?page='
    jsonFile = 'dataBase/articles.json'
    articles = {}
    if online:
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
                    uriArticleID = table.find(
                        'a', {'class': 'statement-link'})['href']
                    idPattern = re.search(r'/([0-9]+)/', uriArticleID)
                    idNumber = idPattern.group(1)
                    articles[idNumber] = {
                        'url': url+uriArticleID,
                    }
                if idNumber == str(215):
                    break
            if idNumber == str(215):
                break

        with open(jsonFile, 'w') as file:
            # la sortie de Json est une variable ici c'est a
            json.dump(articles, file, indent=2, ensure_ascii=False)
    else:
        with open(jsonFile) as file:
            articles = json.load(file)
    return articles


# creatio, d'un fichier JSON pour stocker tout les pages recupéréer (titre et links)


def writeLinksJson(article, append=False):
    file = 'dataBase/articles.json'
    if append:
        with open(file, 'a+') as jsonOut:
            json.dump(article, jsonOut, indent=2, ensure_ascii=False)
    else:
        with open(file, 'w+') as jsonOut:
            json.dump(article, jsonOut, indent=2, ensure_ascii=False)
            # ensure_ascii=False : pour bien afficher les caractéres accentueux


def readLinksJson():
    file = 'dataBase/articles.json'
    if os.path.isfile(file):
        with open(file) as jsonIn:
            data = json.load(jsonIn)
            return data
    else:
        print("I can't find ", file)


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
    url = 'https://pagellapolitica.it/'
    if online:
        uriArticle = 'dichiarazioni/'
        address = url + uriArticle + id
        print(address)
        resp = requests.get(address)
        if resp:
            source = requests.get(address).text
            soup = bs.BeautifulSoup(source, "lxml")

            # auteur
            p = soup.find(
                'p', {'class': 'h4 mb-1 px-2 text-dark font-weight-light'})
            author = p.find('a', {'class': 'u-link-muted'}).text.strip()

            # le titre au complet quand on rentre dans l'article
            divFullBody = soup.find('div', {'class': 'col-lg-9 mb-9 mb-lg-0'})
            if divFullBody:
                # veracity
                # h2 mark-ni
                # h2 mark-vero
                # h2 mark-ceri
                # h2 mark-pinocchio
                # h2 mark-panzana

                veracities = ["mark-ni", "mark-vero",
                              "mark-ceri", "mark-pinocchio", "mark-panzana"]
                divTitle = divFullBody.find('div', {'class': 'mb-2 mt-2 px-2'})
                divTitlePH2Px2 = divFullBody.find(
                    'p', {'class': 'h2 px-2'})
                if divTitle:
                    fullTitle = divTitle.find(
                        'span', {'class': 'h2'}).text.strip()

                    spanVeracity = divTitle.find(
                        'span', {'class': 'h2'})
                    thisVeracity = spanVeracity['class']
                    veracity = common(thisVeracity, veracities)[0]
                elif divTitlePH2Px2:
                    fullTitle = divTitlePH2Px2.find(
                        'span', {'class': 'text-darker'}).text.strip()
                    spanVeracity = divTitlePH2Px2.find(
                        'span', {'class': 'text-darker'})
                    thisVeracity = spanVeracity['class']
                    veracity = common(thisVeracity, veracities)[0]

                else:
                    # dans les anciens artictles le fullText n'existe pas donc
                    # si il ne le trouve pas il affiche le msg
                    fullTitle = "No fullTitle"
                    veracity = "No veracity"

            # les claims
            pclaimPX3 = soup.find(
                'p', {'class': 'lead px-3 py-3 bg-light g-brd-around g-brd-lightblue'})
            pclaimPX2 = soup.find('p', {'class': 'h2 px-2'})
            if pclaimPX3:
                claim = pclaimPX3.text.strip()
            elif pclaimPX2:
                claim = pclaimPX2.find(
                    'span', {'class': 'text-darker'}).text.strip()

            # les dates(publication,origine) elles sont dans la méme classe d'ou l'utilisation
            # de divDates[0] pour la publication et divDates[1] pour l'origine
            divDate = soup.find('div', {'class': 'card-body pt-0 px-2'})
            divDates = divDate.findAll('div', {'class': 'col-lg-2 text-left'})
            datePublished = divDates[0].find(
                'span', {'class': 'text-dark'}).text.strip()
            dateOrigin = divDates[1].find(
                'span', {'class': 'text-dark'}).text.strip()

            # statement source
            divReferredLinks = divDate.find('div', {'class': 'col-lg-4'})
            statementSource = divReferredLinks.find(
                'a', {'class': 'u-link-muted'})['href']

            # le join est pour concaténé les textes des balises P pour les mettre en un seul txt
            divMainArticle = soup.find('div', {'id': 'analisi-content'})
            listOfPInMainArticle = divMainArticle.findAll('p')
            mainText = [text.text.strip() for text in listOfPInMainArticle]
            mainArticle = ' '.join(mainText)

            # les liens de reference dans le main text
            # listOfAllLinks = divMainArticle.findAll('a')
            listOfAllLinksHref = [link['href']
                                  for link in divMainArticle.findAll('a', href=True)]

            # Tags
            if divFullBody.find('div', {'class': 'px-2 u-space-2-top'}):
                divTags = divFullBody.find(
                    'div', {'class': 'px-2 u-space-2-top'})
                tags = divTags.findAll(
                    'a', {'class': 'btn btn-sm btn-light u-btn-light transition-3d-hover rounded-0 mb-2'})

                tagList = []
                for tag in tags:
                    tagList.append(tag.text.strip())

    else:
        data = readLinksJson()
        # pour l'ajout d'un element dans un dictionnaire exsitant ,**dic[2] recupére
        # tout les anciens elements du dic
        data[id] = {
            **data[id],
            # le site de fact checking
            "source": "source not found",
            "claim": "claim not found",
            "body": "mainArticle not found",                     # le text de l'article
                    "referred_links": "listOfAllLinksHref not found",    # tous les liens dans le texte
                    "title": "fullTitle not found",                      # le titre de l'article
                    "date": "dateOrigin not found",                      # date de la claim
                    "url": "address not found",  # url de l'article
                    "tags": "tags not found",                          # les mots cles
                    "author": "author not found",                       # auteur de la claim
                    "datePublished": "datePublished not found",
                    "rating_value": "rating_value not found",          # la valeur de la veracite
                    "statementSource": "statementSource not found",
                    # les entities nomes qui est extraite de la claim
                    "claim_entities": "claim_entities not found",
                    # les entities nomes qui est extraite de l'article
                    "body_entities": "body_entities not found",
                    # parmi les tages, les entities nomes a partir de la tag
                    "keyword_entities": "keyword_entities not found",
                    # les entities nomes a partir de l'auteur de la claim
                    "author_entities": "author_entities not found",
                    "review_author": "review_author not found"         # l'auteur de l'article

        }

    article = {
        id: {
            "source": url,                           # le site de fact checking
            "claim": claim,
            "body": mainArticle,                     # le text de l'article
            "referred_links": listOfAllLinksHref,    # tous les liens dans le texte
            "title": fullTitle,                      # le titre de l'article
            "date": dateOrigin,                      # date de la claim
            "url": address,  # url de l'article
            "tags": tagList,                          # les mots cles
            "author": author,                       # auteur de la claim
            "datePublished": datePublished,
            "rating_value": veracity,          # la valeur de la veracite
            "statementSource": statementSource,
            # les entities nomes qui est extraite de la claim
            "claim_entities": "claim_entities not found",
            # les entities nomes qui est extraite de l'article
            "body_entities": "body_entities not found",
            # parmi les tages, les entities nomes a partir de la tag
            "keyword_entities": "keyword_entities not found",
            # les entities nomes a partir de l'auteur de la claim
            "author_entities": "author_entities not found",
            "review_author": "review_author not found"         # l'auteur de l'article

        }
    }

    return article

# pour lire le contenue de JSON


def pageLinks(pageNumber):
    url = 'https://pagellapolitica.it/'
    uri = 'dichiarazioni/verificato?page='
    pageAddress = url + uri + pageNumber
    resp = requests.get(pageAddress)
    if resp:
        source = requests.get(pageAddress).text
        soup = bs.BeautifulSoup(source, "lxml")
        tables = soup.findAll('div', {'class': 'col-lg-3 mb-7'})
        pageLinks = []
        for table in tables:
            link = table.find('a', {'class': 'statement-link'})['href']
            articleLink = url+link
            pageLinks.append(articleLink)
    return pageLinks


def idNumber(link):
    idPattern = re.search(r'/([0-9]+)/', link)
    idNumber = idPattern.group(1)
    return idNumber


def findPageNumberOfID(id):
    for pageNumber in range(1, 200):
        print("Page:", pageNumber)
        pageLinks = library.extraction.pageLinks(str(pageNumber))
        for page in pageLinks:
            idWanted = library.extraction.idNumber(page)
            if idWanted == id:
                print("ID", id, "is in the page:", pageNumber)
                break
        if idWanted == id:
            break

def accumulate(*args):
    res = ""
    for sentence in args:
        res += sentence + " "
    return res

