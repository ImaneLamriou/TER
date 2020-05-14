import bs4 as bs
import requests
import logging
import tagme
import json
import sys
import os
import re

# *************************** Tagme configurations *******************
tagme.GCUBE_TOKEN = "7d611b53-1694-4c90-8b18-8ba26a30c03b-843339462"
program = os.path.basename(sys.argv[0])
logger = logging.getLogger(program)
logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
language = "it"
# ********************************************************************


def common(a, b):
    """
    This method will get two lists and will return a List of common elements
    between both of them .
    """
    c = [value for value in a if value in b]
    return c


def common2(a, b):
    """
    This method will get two lists and will return a Set of common elements
    between both of them.
    """
    return set(a).intersection(b)


def removePunctuation(string):
    """
    This method will get an string and will return the string without any
    punctuations.
    """
    result = re.sub('[«»!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~]', '', string)
    return result


# Vero              = 1         = mark-vero
# C'eri quasi       = 2         = mark-ceri
# Ni                = 3         = mark-ni
# Pinocchio andante = 4         = mark-pinocchio
# Panzana pazzesca  = 5         = mark-panzana


def frenchVeracity(veracity):
    """
    This method will get a veracity in Italian and will return it's
    translation in French.
    """
    db = {'mark-vero': 'Vrai', 'mark-ceri': 'Quasi-Vrai', 'mark-ni': 'Faux',
          'mark-pinocchio': 'Presque-Faux', 'mark-panzana': 'Archi-Faux'}
    veracityResult = db.get(veracity, 'Faux')
    return veracityResult


def linksOfpagellapolitica(online=False):
    """
    Create historical data from the beginning to the present day.
    """
    idNumber = 0
    url = 'https://pagellapolitica.it/'
    uriPage = 'dichiarazioni/verificato?page='
    # maxsize : c'est pour prendre toutes les pages depuis 2012
    articles = {}
    totalNumberOfArticles = 1
    for i in range(sys.maxsize):
        pageNumber = i
        pageNumber = str(pageNumber)
        address = url + uriPage + pageNumber
        print("Page:", i+1, "\n", "*"*50)

        # si la resp est=200(pas d'erreur) on passe au if
        resp = requests.get(address)
        if resp:
            source = requests.get(address).text
            soup = bs.BeautifulSoup(source, "lxml")
            tables = soup.findAll('div', {'class': 'col-lg-3 mb-7'})

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
                articleData = extractInfoArticle(idNumber, online)
                articles.update(articleData)
                # print(totalNumberOfArticles, idNumber, shortTitle)
                print(idNumber)
                totalNumberOfArticles += 1

                # le if ici c'est pour arreter la boucle car elle tourne
                # indefiniment méme si l'ID n'existe pas
                if idNumber == str(215):
                    break
        if idNumber == str(215):
            break

    print("Harvesting is finished successfully.")
    return articles


def articleLinkIdGenerator(online=False):
    """
    This function will get the state of online or offline and will return a 
    dictionary contain all article's ID in the website.
    """
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
    """
    This function will get a data and the state of append and will write in a
    new json file or at the end of an existing json file.
    """
    file = 'dataBase/pagellapolitica.json'
    if append:
        with open(file, 'a+') as jsonOut:
            json.dump(article, jsonOut, indent=2, ensure_ascii=False)
    else:
        with open(file, 'w+') as jsonOut:
            json.dump(article, jsonOut, indent=2, ensure_ascii=False)
            # ensure_ascii=False : pour bien afficher les caractéres accentueux


def readLinksJson():
    """
    This function will read and return data read from json file.
    """
    file = 'database/pagellapolitica.json'
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
    """
    This function will get an ID number and the state of online or offline and
    will return a dictionary of all information about that article.
    """
    article = {}
    url = 'https://pagellapolitica.it/'
    if online:
        uriArticle = 'dichiarazioni/'
        address = url + uriArticle + id
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
                    veracityItalien = common(thisVeracity, veracities)[0]
                    veracity = frenchVeracity(veracityItalien)
                elif divTitlePH2Px2:
                    fullTitle = divTitlePH2Px2.find(
                        'span', {'class': 'text-darker'}).text.strip()
                    spanVeracity = divTitlePH2Px2.find(
                        'span', {'class': 'text-darker'})
                    thisVeracity = spanVeracity['class']
                    veracityItalien = common(thisVeracity, veracities)[0]
                    veracity = frenchVeracity(veracityItalien)

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
            mainArticleWithPunctuaion = ' '.join(mainText)
            mainArticle = removePunctuation(mainArticleWithPunctuaion)

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


def linksInPage(pageNumber):
    """
    This function will get a page number and will return all article's links 
    found in that page. 
    """
    url = 'https://pagellapolitica.it/'
    uri = 'dichiarazioni/verificato?page='
    pageAddress = url + uri + pageNumber
    resp = requests.get(pageAddress)
    if resp:
        source = requests.get(pageAddress).text
        soup = bs.BeautifulSoup(source, "lxml")
        tables = soup.findAll('div', {'class': 'col-lg-3 mb-7'})
        linksInPage = []
        for table in tables:
            link = table.find('a', {'class': 'statement-link'})['href']
            articleLink = url+link
            linksInPage.append(articleLink)
    return linksInPage


def idNumber(link):
    """
    This function will get a URL and will return it's ID number. 
    """
    idPattern = re.search(r'/([0-9]+)/', link)
    idNumber = idPattern.group(1)
    return idNumber


def findPageNumberOfID(id):
    """
    This function will get an article ID and will return it's page number. This method is writen just for debugging porpose.
    """
    for pageNumber in range(1, 200):
        print("Page:", pageNumber)
        links = linksInPage(str(pageNumber))
        for link in links:
            idWanted = idNumber(link)
            if idWanted == id:
                print("ID", id, "is in the page:", pageNumber)
                break
        if idWanted == id:
            break


def accumulate(*args):
    """
    This function will get a list of strings as parameters and will return an accumulate string of all elements in the list. 
    """
    res = ""
    for sentence in args:
        res += sentence + " "
    return res


def listToString(list):
    """
    Accumulate a list of string elements to an string.
    """
    res = " ".join(list)
    return res


def Annotation_mentions(txt):
    """
    Discover the concepts of wiki concept entities in those texts
    :param txt: a text object, str type
    :return: key-value pair, the key is the original entity concept in this article, the value is the concept size of the concept as a wiki concept, and those that belong to the wiki concept but have ambiguity also include
    """
    annotation_mentions = tagme.mentions(txt)
    dic = dict()
    for mention in annotation_mentions.mentions:
        try:
            dic[str(mention).split(" [")[0]] = str(mention).split("] lp=")[1]
        except:
            logger.error('error annotation_mention about ' + mention)
    return dic


def Annotate(txt, language="en", theta=0.1):
    """
         Solving the mapping problem between conceptual entities of text and Wikipedia concepts
         :param txt: a text object, str type
         :param language: The language used "de" is German, "en" is English, "it" is Italian. The default is English "en"
         :param theta: threshold [0, 1], select the label score, the larger the threshold, the more reliable the filtered map, the default is 0.1
         :return: key-value pair [(A, B):score] A is the conceptual entity in the text, B is the wiki concept entity, and score is the score
    """
    annotations = tagme.annotate(txt, lang=language)
    dic = dict()
    for ann in annotations.get_annotations(theta):
        # print(ann)
        try:
            A, B, score = str(ann).split(" -> ")[0], str(ann).split(" -> ")[1].split(
                " (score: ")[0], str(ann).split(" -> ")[1].split(" (score: ")[1].split(")")[0]
            dic[(A, B)] = score
        except:
            logger.error('error annotation about ' + ann)
    return dic


def wikiLinks(text, language="it"):
    """
    This function will get an string as a parameter and will return a list of all found entities.
    """
    listOfLinks = []
    obj = tagme.Annotation_mentions(text)
    for namedIdentity in obj.keys():
        norm_title = tagme.normalize_title(namedIdentity)
        wikiTitle = tagme.wiki_title(norm_title)
        url = tagme.title_to_uri(wikiTitle, lang=language)
        listOfLinks.append(url)
    return listOfLinks


# **************************** Main *********************************


# ************************************************
# History data to JSON using linksInPage()
# ************************************************

# articleNumber = 0
# for pageNumber in range(1, 200):
#     print("*"*50)
#     print("Page:", pageNumber)
#     print("*"*50)
#     links = linksInPage(str(pageNumber))
#     for link in links:
#         id = idNumber(link)
#         articleNumber += 1
#         print("\n", articleNumber)
#         lastArticle = extractInfoArticle(id, online=True)
#         writeLinksJson(lastArticle, append=True)

# ************************************************
# JSON to CSV
# ************************************************

# jsonDatabase = "database/pagellapolitica.json"
# csvDatabase = "pagellapolitica.csv"
# with open(jsonDatabase, "r") as jsonFile:
#     df = pd.read_json(jsonFile).T

# df.to_csv(csvDatabase)


# ************************************************
# History data to JSON using linksOfpagellapolitica()
# ************************************************

data = linksOfpagellapolitica(online=True)
writeLinksJson(data, append=False)
