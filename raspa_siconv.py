#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Raspando o SICONV
@author: Neylson
"""
import requests
import time
from selenium import webdriver


url = 'https://transfere.convenios.gov.br/habilitacao/api/entidade?uf=MG&categoria=o&aa=04.2&total&_=1502809681676'
headers = {"Host":"transfere.convenios.gov.br",
        "User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0",
        "Accept":"*/*",
        "Accept-Language":"pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding":"gzip, deflate, br",
        "Content-Type":"application/json",
        "X-Requested-With":"XMLHttpRequest",
        "Referer":"https://transfere.convenios.gov.br/habilitacao/consulta-entidade.html?Usr=guest&Pwd=guest",
        "Cookie":"JSESSIONID=DRn8cdERGCe70KVp+vO3AtB7.transfere1",
        "Connection":"keep-alive"}
s = requests.Session()
r = s.get(url=url, headers = headers, verify=False)
r.json()

with open("instituicoes.txt", "w") as saida:
    saida.write(r.text)


#Pegando os cnpjs
cnpjs = []
for i in range(len(r.json())):
    cnpjs.append(r.json()[i]['cnpj'])


#Fazendo a lista de urls
links = []
for cnpj in cnpjs:
    links.append('https://transfere.convenios.gov.br/habilitacao/api/entidade/'+
                 cnpj+
                 '?completo&_=1502830803040')

headers2 = {'Host': 'transfere.convenios.gov.br',
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36 OPR/47.0.2631.39',
            'Content-Type': 'application/json',
            'Referer': 'https://transfere.convenios.gov.br/habilitacao/consulta-entidade.html?Usr=guest&Pwd=guest',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.6,en;q=0.4',
            'Cookie': 'JSESSIONID=gO2UmeLMI6N3ssvnS04C10cB.transfere1'
            }

#with open("links.txt", "w") as sai:
#    for link in links:
#        sai.write(str(link)+'\n')

# Raspando todas as instituições
saida2 = open("dados_instituicoes3.txt", "w")

#Fazendo com selenium
browser = webdriver.Firefox()
browser.get('https://transfere.convenios.gov.br/habilitacao/consulta-entidade.html?Usr=guest&Pwd=guest')
time.sleep(5)
saida2.write('[')

for link in range(len(links)): #len(links)
    print(link)
    print("Abrindo o link...")
    browser.get(links[link])
    time.sleep(5)
    print("Abre raw data...")
    raw_data = browser.find_element_by_class_name('rawdata')
    raw_data.click()
    print("Capturando e gravando...")
    data = browser.find_element_by_class_name('data')
    saida2.write(data.text+',')
    time.sleep(2)

print("Pronto!")
print("Finalizando o arquivo dados_instituicoes.txt .......")
saida2.write(']')

saida2.close()

