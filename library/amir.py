import bs4 as bs
import requests
import os
import re
import sys
import json
import extraction as ter


dic = {
    1: {
        "Name": "Amir",
        "Family": "SHIRALI POUR",
        "Cell Phone": "0628299022"
    }
}

print("Cell Phone = ", dic[1]["Cell Phone"])

imane = {2: {
    "Name": "Imane",
    "Family": "Lamriou",
    "Cell Phone": "0767456609*"
}}

dic.update(imane)

# pour l'ajout d'un element dans un dictionnaire exsitant ,**dic[2] recupére
# tout les anciens elements du dic
dic[2] = {**dic[2], "class": "21254465"}


with open('amir.json', 'w') as myJson:
    json.dump(dic, myJson, indent=2)
