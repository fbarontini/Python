import requests, csv
from datetime import datetime
from bs4 import BeautifulSoup

URL = ['http://nomesportugueses.blogspot.com.br/p/nomes-brasileiros-de-z.html',
       'http://nomesportugueses.blogspot.com.br/2009/04/nomes-masculinos-de-a-z.html',
       'http://nomesportugueses.blogspot.com.br/2009/04/nomes-femininos-de-a-z.html',
       'http://nomesportugueses.blogspot.com.br/p/nomes-estrangeiros.html']
nomes = []


def getContent(linkURL):
    
    response = requests.get(linkURL)
    html = response.text
    # insere o HTML no Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')
    
    return soup.find_all("ul")


def addNomes(content):
    for ul in content:
        for name in ul.find_all('li'):
            nomes.append(name.text)


for url in URL:
    conteudo = getContent(url)
    addNomes(conteudo)


with open('C:\\temp\index.csv', 'a') as csv_file:
    writer = csv.writer(csv_file)
    
    for nome in nomes:
        writer.writerow([nome])