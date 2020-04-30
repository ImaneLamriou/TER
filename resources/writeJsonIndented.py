import json
import bs4
import requests
import lxml


file = "tags"
ext = ".json"
file1 = file + ext
file2 = file + "_out" + ext
with open(file1, 'r') as fileIn:
    data = json.load(fileIn)

with open(file2, 'w') as fileOut:
    json.dump(data, fileOut, indent=2)

with open(file2) as file:
    data = json.load(file)


# print("Data size:", len(data))

# print(data[0]["_links"]["author"][0]['href'])

# url = data[0]["_links"]["author"][0]['href']

# response = requests.get(url).json()

# print(response['name'])


# with open("first.json", 'w') as fileOut:
#     json.dump(data[0], fileOut, indent=2)
