import bs4 as bs
import requests
import os
# import re

# recuperation de toutes les pages depuis la création du site
os.system("cls")

url = 'https://pagellapolitica.it/'
uri = 'dichiarazioni/verificato'
address = url + uri
print("Address:", address)

source = requests.get(url).text
soup = bs.BeautifulSoup(source, "lxml")
tables = soup.findAll('div', {'class': 'col-lg-3 mb-7'})
