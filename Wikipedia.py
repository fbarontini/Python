# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup as Bs
from time import sleep

def captura_titulo():

    url = 'https://pt.wikipedia.org/wiki/Especial:Aleat%C3%B3ria'
    # rotina para capturar o titulo
    req = requests.get(url)
    sleep(3)
    # converto para uma variavel do tipo BeautifulSoup
    soup = Bs(req.text, 'html.parser')
    # encontro a tag H1
    tag = soup.find('h1')
    # extraio o texto da tag
    titulo = tag.get_text()
    
    return titulo

def captura_url():

    url = 'https://pt.wikipedia.org/wiki/Especial:Aleat%C3%B3ria'
    # rotina para capturar o titulo
    req = requests.get(url)
    sleep(3)
    # converto para uma variavel do tipo BeautifulSoup
    soup = Bs(req.text, 'html.parser')
    # encontro a tag H1
    tag = soup.find('h1')
    # extraio o texto da tag
    titulo = tag.get_text()
    
    return titulo, req.url

TITULOS = []
'''
    Para uma sequencia de 10, insira 10 titulos 
    na variavel TITULOS
'''
n = 10

for i in range(n):
    # insiro o titulo aqui
    #TITULOS.append(captura_titulo())
    
    d = {}
    t,u = captura_url()
    d['titulo'] = t
    d['url'] = u
    print(d)
    TITULOS.append(d)