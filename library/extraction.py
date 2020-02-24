import bs4 as bs
import requests
import os
import re
import sys

os.system("clear")


def linksOfpagellapolitica():
    url = 'https://pagellapolitica.it/'
    uri = 'dichiarazioni/verificato?page='
    for i in range(sys.maxsize):
        pageNumber = i
        pageNumber = str(pageNumber)
        address = url + uri + pageNumber
        print("address:", address)
