BASE DE DATOS

En el archivo 'Base_de_datos.py' se encuentra:

- El SCRAPING de la WEB para la obtencion de los datos
- La limpieza de los datos
- La filtración de las distintas caracteristicas en distintas columnas
- El cruce del componente PROCESADOR con una base de datos externa con el fin de establecer un ranking inicial


En el archivo 'Guardar_base_de_datos.py' se encuentra:
- La creación del dataframe
- Guardado del dataframe en formato CSV (para posterior tratamiento de los datos)
- Guardado del dataframe en formato XML (para visualizacion rapida de los datos)
- Al archivo excel se le ha asociado una MACRO ('vbaProject.bin') que se activa con la combinación de teclas CTRL + A. La MACRO arregla únicamente aspectos visuales con el fin de que la visualización rápida sea más comoda
