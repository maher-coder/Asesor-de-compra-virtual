# -*- coding: utf-8 -*-
"""
Created on Wed May 5 18:25:53 2020

@author: MAHER
"""

import pandas as pd
import ast
import numpy as np
from tqdm.notebook import tqdm
import re

#Leemos el csv que hemos generado con anterioridad
df = pd.read_csv(r'C:\Users\MAHER\Desktop\PROGRAMACIÓN\Py Programming\Portatiles PC componentes\Base de datos\Portatiles 2020-05-05.csv')

#Eliminamos los espacios y los parentesis de los nombres para que sea más facil el tratamiento de datos
df.rename(columns={'Ranking Procesador': 'Ranking_Procesador', 'RAM (GB)': 'RAM_GB', 'Disco duro': 'Disco_duro', 'Precio(€)': 'Precio'}, inplace = True)

#Eliminamos los portatiles con precio erroneo
df = df[df['Precio']>=15]
df.reset_index(drop=True, inplace = True)


#Arreglamos las variables y procedemos a crear los parametros de valoración
Procesador_arreglado = np.zeros(len(df), dtype = np.float32)
ram_arreglado = np.zeros(len(df), dtype = np.float16)
disco_arreglado = np.zeros(len(df), dtype = np.float32)
ssd = np.zeros(len(df), dtype = np.bool)
for num, row in enumerate(tqdm(df[['Procesador', 'Ranking_Procesador', 'RAM_GB', 'Disco_duro']].itertuples(), total=df.shape[0])):
    
    if str(row.Ranking_Procesador).isdigit():
        Procesador_arreglado[num] = row.Ranking_Procesador
    else:
        try:
            primero = ast.literal_eval(row.Ranking_Procesador)[0][0]
            try:
                segundo = ast.literal_eval(row.Ranking_Procesador)[1][0]
            except:
                segundo = primero
            Procesador_arreglado[num] = (primero + segundo)/2
        except:
            Procesador_arreglado[num] = np.nan
    
    
    try:
        ram_arreglado[num] = sum(list(map(int,re.findall("\d+", row.RAM_GB))))
    except:
        ram_arreglado[num] = np.nan
        
        
    try:
        temp = list(map(int,re.findall("\d+", row.Disco_duro)))
        if len(temp) == 2:
            if temp[0]<10:
                temp[0] = temp[0]*1000
                disco_arreglado[num] = sum(temp)
            else:
               disco_arreglado[num] = sum(temp) 
        else:
            temp = sum(temp)
            if temp<10:
                disco_arreglado[num] = temp*1000
            else:
                disco_arreglado[num] = temp
    except:
        disco_arreglado[num] = np.nan
        
    #Booleano de si tiene o no ssd
    try:
        if ('SSD' in row.Disco_duro) or ('ssd' in row.Disco_duro):
            ssd[num] = True
        elif ('HDD' in row.Disco_duro) or ('hdd' in row.Disco_duro):
            ssd[num] = False
        else:
            ssd[num] = False
    except:
        ssd[num] = False
    
extra_df = pd.DataFrame({'Procesador_arreglado': Procesador_arreglado,
                         'ram_arreglado': ram_arreglado,
                         'disco_arreglado': disco_arreglado,
                         'ssd': ssd})
df = pd.concat([df, extra_df], axis = 1)

df.dropna(subset=['Procesador_arreglado', 'ram_arreglado', 'disco_arreglado', 'ssd'], inplace = True)
df.reset_index(drop=True, inplace = True)


parametro_1 = np.zeros(len(df), dtype = np.float32)
parametro_2 = np.zeros(len(df), dtype = np.float32)
parametro_3 = np.zeros(len(df), dtype = np.float32)
for num, row in enumerate(tqdm(df[['Precio', 'Procesador_arreglado', 'ram_arreglado', 'disco_arreglado', 'ssd']].itertuples(), total=df.shape[0])):
    parametro_1[num] = row.Precio/row.ram_arreglado
    parametro_2[num] = row.Procesador_arreglado/row.Precio
    if row.ssd:
        '''
        Equivalencia de precio SSD-HDD
        256 GB SSD = 3 TB HDD
        '''
        parametro_3[num] = (row.Precio*256)/row.disco_arreglado
    else:
        parametro_3[num] = (row.Precio*3000)/row.disco_arreglado
extra_df = pd.DataFrame({'parametro_1': parametro_1,
                         'parametro_2': parametro_2,
                         'parametro_3': parametro_3})
df = pd.concat([df, extra_df], axis = 1)

df['parametro_1'] = df['parametro_1']/max(df['parametro_1'])
df['parametro_2'] = df['parametro_2']/max(df['parametro_2'])
df['parametro_3'] = df['parametro_3']/max(df['parametro_3'])

df['valoración_1'] = (df['parametro_1']+df['parametro_2']+df['parametro_3'])/3
df['valoración_2'] = (df['parametro_1']*df['parametro_2']*df['parametro_3'])**(1/3)
df['valoración_3'] = (df['parametro_1']*df['parametro_2']*df['parametro_3'])/(df['parametro_1']*df['parametro_2']+df['parametro_1']*df['parametro_3']+df['parametro_2']*df['parametro_3'])

df['valoración'] = (df['valoración_1']+df['valoración_2']+df['valoración_3'])/2



precio_max = float(input('Introduce tu presupuesto = '))
df = df[df['Precio']<=precio_max]
df.sort_values(by = 'valoración', axis=0, ascending=True, inplace=True)
df.reset_index(drop=True, inplace = True)


print('Top 5 mejores portatiles para el presupuesto proporcionado')

for i in range(5):
    print('Nombre: {}'.format(df['Nombre'][i]))
    print(' - Procesador: {}'.format(df['Procesador'][i]))
    print(' - RAM: {}'.format(df['RAM_GB'][i]))
    print(' - Memoria: {}'.format(df['Disco_duro'][i]))
    print(' - Pantalla: {}"'.format(re.findall("\d+", df['Pantalla'][i])[0]))
    print(' - GPU: {}'.format(df['Gráfica'][i]))
    print(' - Precio: {}€'.format(df['Precio'][i]))
    print('')