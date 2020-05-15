import bs4
import requests
import os
import re
import sys
import json
import pandas as pd


def linkArticles(online=False):
    jsonLinks = "database/AfricaCheck_links.json"
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
        with open(jsonLinks, 'w') as file:
            json.dump(links, file, indent=2)
    else:
        with open(jsonLinks, 'r') as file:
            links = json.load(file)

    print("Total Number Of Articles:", totalNumberOfArticles)
    return links


def beautifulObject(link):
    # on recupere le code source de page dans la variable source avec .text a la fin
    source = requests.get(link).text
    soup = bs4.BeautifulSoup(source, "lxml")
    # div = soup.find('div', {'class': 'report-verdict'})
    if soup:
        return soup
    else:
        return None


def title(soup):
    title = "No Title"
    if soup:
        header = soup.find('header', {'class': 'article-header clearfix'})
        title = header.find('h1', {'class': 'single-title'}).text

    return title


def claim(soup):
    claim = "No Claim"
    if soup:
        div = soup.find('div', {'report-claim'})
        if div:
            claimTag = div.findAll('p')
            claim = claimTag[0].text.strip()

    return claim


def veracity(soup):
    veracity = "No Veracity"
    if soup:
        div = soup.find('div', {'class': 'report-verdict'})
        if div:
            veracity = div.find('div', {'class': 'verdict-stamp'}).text

    return veracity


def datePublished(soup):
    if soup:
        div = soup.find('div', {'class': 'col-sm-12 time-subscribe-wrapper'})
        datePublished = div.find('time')['datetime'][:10]
    else:
        datePublished = 'No datePublished'
    return datePublished


def tags(soup):
    if soup:
        tagsTag = soup.findAll('meta', attrs={'property': 'article:tag'})
        tag_list = []
        for tag in tagsTag:
            tag_text = tag['content']
            tag_list.append(tag_text)
    else:
        tag_list = []
    return tag_list


def mainArticle(soup):
    if soup:
        section = soup.find('section', {'class': 'entry-content clearfix'})
        article = section.findAll('p')
        mainText = [text.text.strip() for text in article]
        mainArticleWithPunctuaion = ' '.join(mainText)
        mainArticle = removePunctuation(mainArticleWithPunctuaion)
    else:
        mainArticle = "No Body"
    return mainArticle


def referredLinks(soup):
    if soup:
        article = soup.find('article')
        listOfAllLinksHref = [link['href']
                              for link in article.findAll('a', href=True)]
    else:
        listOfAllLinksHref = "No referredLinks"
    return listOfAllLinksHref


def claimParagraphe(soup):
    author = "No Author"
    if soup:
        sectionArticle = soup.find(
            'section', {'class': 'entry-content clearfix'})
        author = sectionArticle.find('p')

    return author


def review_author(soup):
    if soup:
        authorTag = soup.find('p', {'class': 'editor-name'}).text
        review_author = authorTag.replace('Recherché par', '').strip()
    else:
        review_author = "No review_author"
    return review_author


# to complete
def statementDateAndSource(soup):
    author = "No Author"
    date = "No Date"
    if soup:
        divStatement = soup.find('div', {'class': 'report-claim'})
        if divStatement:
            pStatement = divStatement.findAll('p')
            statementSource = pStatement[1]
            if pStatement[1].find('strong'):
                statementSource.strong.decompose()
            mat = re.search(r'\(', statementSource.text)
            if mat:
                authorTag = statementSource.text.split('(')
                date = authorTag[1][:-2].strip()
                author = authorTag[0].strip()
    return author, date


# I found that the first link in the main article that is not a photo is the
# statement source (link) :)
def statementLink(soup):
    statementLink = "No statementLink"
    if soup:
        sectionClaim = soup.find(
            'section', {'class': 'entry-content clearfix'})
        pClaim = sectionClaim.find('p', {'class': None})
        if sectionClaim.find('a'):
            statementLink = sectionClaim.find('a', {'class': None})['href']
        else:
            statementLink = pClaim  # "No statementLink"

    return statementLink


def articleID(soup):
    id = "No id"
    if soup:
        id = shortLink(soup).replace(
            'https://fr.africacheck.org/?p=', '')

    return id


def shortLink(soup):
    shortLink = "No shortLink"
    if soup:
        headTag = soup.find('head')
        shortLink = headTag.find('link', {'rel': 'shortlink'})['href']

    return shortLink


def api(online=False):
    linkV1 = "https://fr.africacheck.org/wp-json/"
    linkV2 = "https://fr.africacheck.org/wp-json/wp/v2"
    posts = "https://fr.africacheck.org/wp-json/wp/v2/posts"

    uri = "https://fr.africacheck.org/wp-json/?p=223333"

    file = "database/posts.json"
    if online:
        data = requests.get(uri).json()
        with open(file, "w") as jsonFile:
            json.dump(data, jsonFile, indent=2)
    else:
        with open(file) as readJson:
            data = json.load(readJson)
    return data


def extract(data):
    print("size of data: ", len(data))


def removePunctuation(string):
    """
    This method will get an string and will return the string without any
    punctuations.
    """
    result = re.sub('[«»!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~]', '', string)
    return result


def writeLinksJson(article, append=False):
    """
    This function will get a data and the state of append and will write in a
    new json file or at the end of an existing json file.
    """
    file = 'dataBase/africacheck.json'
    if append:
        with open(file, 'a+') as jsonOut:
            json.dump(article, jsonOut, indent=2, ensure_ascii=False)
    else:
        with open(file, 'w+') as jsonOut:
            json.dump(article, jsonOut, indent=2, ensure_ascii=False)
            # ensure_ascii=False : pour bien afficher les caractéres accentueux
    print("Harvesting wrote successfully.")


def readLinksJson(links=False):
    """
    This function will read and return data read from json file.
    """
    if links:
        file = 'database/AfricaCheck_links.json'
    else:
        file = 'database/africacheck.json'
    if os.path.isfile(file):
        with open(file) as jsonIn:
            data = json.load(jsonIn)
            return data
    else:
        print("I can't find ", file)


def makeDictionary():
    # premiere ligne de la fonction qui recupere les liens
    links = linkArticles(online=False)
    article = {}

    for i, link in enumerate(links):
        soup = beautifulObject(link)
        id = articleID(soup)
        print(i, id, shortLink(soup))
        print(link, "\n")
        author, date = statementDateAndSource(soup)
        article[id] = {
            "source": "https://fr.africacheck.org/articles",
            "claim": claim(soup),
            "body": mainArticle(soup),
            "referred_links": referredLinks(soup),
            "title": title(soup),
            "datePublished": datePublished(soup),
            "date": date,
            "url": link,
            "shortLink": shortLink(soup),
            "tags": tags(soup),
            "author": author,
            "rating_value": veracity(soup),
            "statementSource": statementLink(soup),
            # les entities nomes qui est extraite de la claim
            "claim_entities": "claim_entities not found",
            # les entities nomes qui est extraite de l'article
            "body_entities": "body_entities not found",
            # parmi les tages, les entities nomes a partir de la tag
            "keyword_entities": "keyword_entities not found",
            # les entities nomes a partir de l'auteur de la claim
            "author_entities": "author_entities not found",
            "review_author": review_author(soup)

        }
    return article


# article = makeDictionary()
# writeLinksJson(article)

data = readLinksJson(links=True)
print("Links:", len(data))
data = readLinksJson(links=False)
print("data online:", len(data))


df = pd.DataFrame(data).T

df.to_csv("database/africacheck.csv", sep=";")

# data = api()
# posts = data
# print(len(posts))
# print(posts[0].keys())
# for post in posts:
#     print(post["id"], "date:", post["date"])
#     # print(post.keys())
