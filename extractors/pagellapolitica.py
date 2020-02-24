import bs4 as bs
import requests
import os
# import re

os.system("cls")

url = 'https://pagellapolitica.it/'
uri = 'dichiarazioni/8531/di-maio-esagera-in-parte-le-eccellenze-italiane'
address = url + uri
print("Address:", address)

# Recupération des URL

# Vero = 1
# C'eri quasi = 2
# Ni = 3
# Pinocchio andante = 4
# Panzana pazzesca = 5


source = requests.get(url).text
soup = bs.BeautifulSoup(source, "lxml")
tables = soup.findAll('div', {'class': 'col-lg-4 mb-7'})

newArticles = {}
i = 1
for table in tables:
    title = table.find('div', {'class': 'mb-0 px-2 min-height-title'})
    title = title.find('span', {'class': 'h6'}).text
    print("title:", title)
    link = table.find('a', {'class': 'statement-link'})['href']
    print("Article", i, "\n = Link:", link, "\nTitle:", title)
    i += 1
