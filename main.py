# -- coding: utf-8 --

'''
pip3 install wget
pip3 install lxml
pip3 install bs4
'''

import requests
import wget
from pathlib import Path
from bs4 import BeautifulSoup

links = []

def getJSON(url):

    r = requests.get(url)
    json_data = r.json()

    # INFINITE
    if (url == "https://en.wikipedia.org/w/api.php?action=query&list=embeddedin&&eilimit=max&eititle=Template:Infobox&format=json"):
        links = []
        while True:
            r = requests.get(url)
            json_data = r.json()
            for i in range(500):
                data = json_data['query']['embeddedin'][i]['title']
                data = data.replace(' ', '_')
                links.append("https://en.wikipedia.org/wiki/"+data)
            infinite = json_data['continue']['eicontinue']
            url = "https://en.wikipedia.org/w/api.php?action=query&list=embeddedin&&eilimit=max" \
                  "&eititle=Template:Infobox&format=json&eicontinue={}".format(infinite)
            createFile(links)

    #DEFINITE NUMBER

    # +500

    #-500
    else:
        for i in range(num):
            links = []
            data = json_data['query']['embeddedin'][i]['title']
            data = data.replace(' ', '_')
            links.append("https://en.wikipedia.org/wiki/"+data)
            createFile(links)

def createFile(links):
    for link in links:
        file_rename = link.replace('https://en.wikipedia.org/wiki/', '')
        file_dest = str(Path.cwd()) + '/pages/'
        file_link = str(file_dest) + str(file_rename)
        wget.download(link, file_dest)

        with open(file_link, 'r') as file:
            data = file.read().replace('\n', '')

        soup = BeautifulSoup(data, 'lxml')
        tag = soup.find('h1', {"class": "firstHeading"}).extract()
        tag2 = soup.find('div', {"id": "bodyContent"}).extract()

        with open(file_link, 'w') as file:
            file.write('<head><link rel="stylesheet" type="text/css" href="../main.css"></head>')
            file.write(str(tag))
            file.write(str(tag2))

        sorted(file_dest)

print()
print("Veuillez définir un nombre de pages à récupérer (entre 1 et 500).")
print("-1, +500 ou rien donnera une recherche continue dans les limites de l'API de Wikipédia.")
print()
num = int(input("Nb de pages : ") or -1)
print()

if num < -1 or num == 0 :
    print("Veuillez indiquer -1 (infini) ou un nombre de pages compris entre 1 et 500.")
else :
    if num > 500 or num == -1:
        url = "https://en.wikipedia.org/w/api.php?action=query&list=embeddedin&&eilimit=max&eititle=Template:Infobox&format=json"
        getJSON(url)
    else :
        url = "https://en.wikipedia.org/w/api.php?action=query&list=embeddedin&&eilimit={}&eititle=Template:Infobox&format=json".format(num)
        getJSON(url)