"""
Created on Fri May  1 21:20:18 2020

@author: MAHER
"""
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import time
import ctypes
import re

url='https://www.pccomponentes.com/portatiles'

#Obtenemos el codigo html de la pagina
page = requests.get(url).text

#Interpretamos el codigo html
soup = BeautifulSoup(page,'lxml')

#Almacenamos el numero total de portatiles
resultados = int(soup.find('div', class_= 'select-redondeado__comparsa').strong.text)



indice = 1

name_procesador = []
ram = []
disco_duro = []
pantalla = []
grafica = []
precio = []
so = []
web = []
#------Obtenemos los datos de la web y los separamos en las distintas caracteristicas que lo componen-----
while len(name_procesador) < resultados:
    
    params = {
        'page': str(indice),
        'order': 'relevance',
        'gtmTitle': 'Portátiles',
        'idFamilies[]': '1115',
    }
    url = 'https://www.pccomponentes.com/listado/ajax?page='+str(indice)+'&order=relevance&gtmTitle=Port%C3%A1tiles&idFamilies%5B%5D=1115'


    page = requests.get(url).text
    #Lo interpretamos como html
    soup = BeautifulSoup(page,'lxml')
    
    for a in soup.find_all("a", class_ = "c-product-card__title-link cy-product-link"):
        
        temp = a['data-name'].split('/')
        precio.append(float(a['data-price']))
        web.append('https://www.pccomponentes.com/')
        so.append('-')
        
        if len(temp) == 6: #en el supuesto de que no se haga el splitting de forma correcta
            name_procesador.append(temp[0])
            ram.append(temp[1])
            disco_duro.append(temp[2])
            grafica.append(temp[3]+' '+temp[4])
            pantalla.append(temp[5])
            
        elif len(temp) ==5:
            name_procesador.append(temp[0])
            ram.append(temp[1])
            disco_duro.append(temp[2])
            grafica.append(temp[3])
            pantalla.append(temp[4])
            
        elif len(temp) ==4:
            name_procesador.append(temp[0])
            ram.append(temp[1])
            disco_duro.append(temp[2])
            grafica.append('')
            pantalla.append(temp[3])
            
        elif len(temp) ==3:
            name_procesador.append(temp[0])
            ram.append(temp[1])
            disco_duro.append(temp[2])
            grafica.append('')
            pantalla.append('')
            
        elif len(temp) ==2:
            name_procesador.append(temp[0]+'/'+temp[1])
            ram.append('')
            disco_duro.append('')
            grafica.append('')
            pantalla.append('')
            
    indice = indice +1
    print('Pagina {} almacenada de Pc Componentes'.format(indice))
    print(name_procesador[-1])
    

#Vamos a separar cada característica del portatil en distintas columnas
    
#-----Separar nombre del procesador-----
nombre = []
procesador = []
no_repartidos = []

for i in range(resultados):
    if 'Intel' in name_procesador[i].split():
        pattern = re.compile(r'Intel')
        matches = pattern.finditer(name_procesador[i])
        for match in matches:
            nombre.append(name_procesador[i][:(match.span()[0]-1)])
            procesador.append(name_procesador[i][match.span()[0]:])
    #    nombre.append(m.group(0))
    elif 'AMD' in name_procesador[i].split():
        pattern = re.compile(r'AMD')
        matches = pattern.finditer(name_procesador[i])
        for match in matches:
            nombre.append(name_procesador[i][:(match.span()[0]-1)])
            procesador.append(name_procesador[i][match.span()[0]:])
    else:
        no_repartidos.append(name_procesador[i])
        intelcore = re.search('i\d', name_procesador[i])

        if 'Core' in no_repartidos[-1]:
            pattern = re.compile(r'Core')
            matches = pattern.finditer(name_procesador[i])
            for match in matches:
                nombre.append(name_procesador[i][:(match.span()[0]-1)])
                procesador.append('Intel ' + name_procesador[i][match.span()[0]:])
            no_repartidos.pop(-1)
            
        elif 'Atom' in no_repartidos[-1]:
            pattern = re.compile(r'Atom')
            matches = pattern.finditer(name_procesador[i])
            for match in matches:
                nombre.append(name_procesador[i][:(match.span()[0]-1)])
                procesador.append('Intel ' + name_procesador[i][match.span()[0]:])
            no_repartidos.pop(-1)
            
        elif intelcore != None:
            pattern = re.compile(r'i\d')
            matches = pattern.finditer(name_procesador[i])
            for match in matches:
                nombre.append(name_procesador[i][:(match.span()[0]-1)])
                procesador.append('Intel ' + name_procesador[i][match.span()[0]:])
            no_repartidos.pop(-1)
        else:
            nombre.append(name_procesador[i])
            procesador.append('')
    #Vamos arreglar el formato de la Ram
    ramformat1 = re.search('\d\dGB', ram[i])
    ramformat2 = re.search('\dGB', ram[i])
    ramformat3 = re.search('\dGb', ram[i])
    if ramformat1 != None :
        ram[i] = ram[i][:2]+' '+ram[i][2:]
    elif ramformat2 != None or ramformat3!= None:
        ram[i] = ram[i][:1]+' '+ram[i][1:]


#Introduciremos un rankig externo de procesadores con el fin de poder clasificar los mismos

#----Ranking de procesadores
n = []
ranking_oficial_procesadores = []
tipo = []
for i in range(1,25):
    url = 'https://technical.city/es/cpu/rating?pg=' + str(i)
    
    page = requests.get(url).text
    
        
    #Interpretamos el codigo html
    soup = BeautifulSoup(page,'lxml')
    
    for i in soup.find_all('td', style = 'text-align:left'):
        ranking_oficial_procesadores.append(i.a.div.img['title'])

    for i in soup.find_all('td', class_= 'rating_list_position'):
        n.append(int(i.text))
    
    for i in soup.find_all('img', class_="type_icon"):
        tipo.append(i['title'])
    
    

        
#------Añadir ranking al df------
import difflib

ranking_procesadores = []
for i in procesador:
    if i in ranking_oficial_procesadores:
        ranking_procesadores.append(n[ranking_oficial_procesadores.index(i)])
    else: #como puede darse el caso de que no este escrito tal cual en el ranking, busca los dos que mas se parezcan
        parecidos = difflib.get_close_matches(i, ranking_oficial_procesadores,n=2,cutoff=0.72)
        ranking_procesadores.append([[n[ranking_oficial_procesadores.index(j)],j] for j in parecidos])