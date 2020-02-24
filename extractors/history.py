import bs4 as bs
import requests
import os
# import re

# recuperation de toutes les pages depuis la création du site
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


