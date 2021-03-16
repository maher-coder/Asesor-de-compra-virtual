"""
Created on Fri May  1 21:20:18 2020

@author: MAHER
"""
#-----Almacenamos datos en excel y en CSV-----

from datetime import date
import pandas as pd
import ctypes

#Día actual
today = date.today()
        
df = pd.DataFrame({'Precio(€)':precio,
                   'Nombre':nombre,
                   'Procesador':procesador,
                   'Ranking Procesador':ranking_procesadores,
                   'RAM (GB)':ram,
                   'Disco duro':disco_duro,
                   'Pantalla':pantalla,
                   'Gráfica':grafica,
                   'Web':web
                   })
df2 = pd.DataFrame({'Nº':n,
                   'Procesador':ranking_oficial_procesadores,
                   'Tipo':tipo
                   })
path = 'C:\\PATH\\Portatiles {}.xlsx'.format(today)

writer = pd.ExcelWriter(path , engine = 'xlsxwriter')
df.to_excel(writer , sheet_name = 'Data Portatiles',index = False)
df2.to_excel(writer , sheet_name = 'Data Ranking Portatiles',index = False)

pandaswb = writer.book
pandaswb.filename = 'C:\\Users\\MAHER\\Desktop\\PROGRAMACIÓN\\Py Programming\\Portatiles PC componentes\\Portatiles {}.xlsm'.format(today)
pandaswb.add_vba_project('C:\\Users\\MAHER\\Desktop\\PROGRAMACIÓN\\Py Programming\\Portatiles PC componentes\\vbaProject.bin')
writer.save()
writer.close()

ctypes.windll.user32.MessageBoxW(0, "Se ha guardado el archivo Portatiles {}.xlsm".format(today), "Información", 1)