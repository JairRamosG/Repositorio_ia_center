import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import os

datos = []
fecha = datetime.datetime.now().strftime("%d-%m-%Y %H_%M_%S")
url = "https://www.cenace.gob.mx/graficademanda.aspx"
clave_region = ["ccbc", "ccbcsur", "cccentral", "ccnoreste", "ccnoroeste", 
                "ccnorte", "ccoccidental", "ccoriental", "ccpeninsular", "sinacional"]

def obtener_contenido(url):
    pagina_web = requests.get(url)
    return pagina_web.content

def genera_soup(contenido_web):
    return BeautifulSoup(contenido_web, "html.parser")

def extraccion_pagina(soup):
          
    for clave in clave_region:
        
      titulo_region = soup.find("li", class_ = clave)
      region = titulo_region.select_one(".titlex").text

      p_tags = soup.select("li." + clave + " p") # Selecciono las 3 etiquetas p
      for p_tag in p_tags:
            if "Demanda Neta:" in p_tag.text:
                 demanda_neta = float(p_tag.select_one(".bold").text.replace(",","")[:-3]) 
            elif "Generación Neta:" in p_tag.text:
                 generacion_neta = float(p_tag.select_one(".bold").text.replace(",","")[:-3])
            elif "Pronóstico Neto:" in p_tag.text:
                 pronostico_neto = p_tag.select_one(".bold").text.replace(",","")[:-3]     
               
      datos.append({
              "Fecha" : fecha,
              "Región": region,
              "Generación Neta MW" : generacion_neta,
              "Demanda Neta MW" : demanda_neta,
                })
      
    return pd.DataFrame(datos)

def actualizar_datos(df):

    documentos = os.listdir("../csv_se")
    n_update = int(documentos[-1].split()[0])
    new_n_update = str(n_update + 1)
    ultimo = documentos[-1]
    fecha_actual = fecha

    df_base = pd.read_csv("../csv_se/" + ultimo)
    df_nuevo = pd.concat([df_base,df], ignore_index=True)

    columnas = ["Fecha", "Región", "Generación Neta MW", "Demanda Neta MW", "Diferencia MW"]
    df_nuevo = df_nuevo[columnas]
    df_nuevo.to_csv("../csv_se/" + new_n_update + " " + fecha_actual + ".csv")

def proceso_datos(url):
    contenido_web = obtener_contenido(url)
    soup = genera_soup(contenido_web)
    df = extraccion_pagina(soup)
    actualizar_datos(df)  

proceso_datos(url)