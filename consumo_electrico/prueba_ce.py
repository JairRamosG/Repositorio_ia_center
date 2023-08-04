# %%
import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import os

# %%
url = "https://www.cenace.gob.mx/graficademanda.aspx"
clave_region = ["ccbc", "ccbcsur", "cccentral", "ccnoreste", "ccnoroeste", 
                "ccnorte", "ccoccidental", "ccoriental", "ccpeninsular", "sinacional"]
datos = []
fecha = datetime.datetime.now().strftime("%d-%m-%Y %H_%M_%S")

# %%
def obtener_contenido(url):
    pagina_web = requests.get(url)
    return pagina_web.content

# %%
def genera_soup(contenido_web):
    return BeautifulSoup(contenido_web, "html.parser")

# %%
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
               
      datos.append({
              "Fecha" : fecha,
              "Región": region,
              "Generación Neta MW" : generacion_neta,
              "Demanda Neta MW" : demanda_neta,
              "Diferencia MW" : generacion_neta - demanda_neta
              })
      
    return pd.DataFrame(datos)
    

# %%
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

# %%
def proceso_datos(url):
    contenido_web = obtener_contenido(url)
    soup = genera_soup(contenido_web)
    df = extraccion_pagina(soup)
    actualizar_datos(df)    

# %%
proceso_datos(url)

# %%
documentos = os.listdir("../csv_se")
ultimo = documentos[-1]
df = pd.read_csv("../csv_se/" + ultimo)
df = df[["Fecha", "Región", "Generación Neta MW", "Demanda Neta MW", "Diferencia MW"]]
df = pd.DataFrame(df)
df

# %%
df_central = df[df["Región"] == "S.I. NACIONAL"]
df_central

# %%
df_central["Fecha"] = pd.to_datetime(df_central["Fecha"], format="%d-%m-%Y %H_%M_%S")
df_central["Hora"] = df_central["Fecha"].dt.strftime("%H")
df_central["Día"] = df_central["Fecha"].dt.strftime("%d-%m-%Y")
df_central

# %%
import matplotlib.pyplot as plt
import numpy as np

# %%
media_generacion = round(df_central["Generación Neta MW"].mean(),2)
media_demanda = round(df_central["Demanda Neta MW"].mean(), 2)
max_demanda = max(df_central["Demanda Neta MW"])
min_demanda = min(df_central["Demanda Neta MW"])
media_demanda = np.mean(df_central["Demanda Neta MW"])
max_generacion = max(df_central["Generación Neta MW"])
min_generacion = min(df_central["Generación Neta MW"])
media_generacion = np.mean(df_central["Generación Neta MW"])
puntos_medios = (df_central["Generación Neta MW"] + df_central["Demanda Neta MW"])/2
dia = df_central["Día"].iloc[-1]
hora = df_central["Hora"].iloc[-1]

# %%
plt.figure(figsize=(15, 6)) 

# Generación
plt.plot(df_central["Hora"], df_central["Generación Neta MW"], label = "Generación", color = "blue")
plt.axhline(y=media_generacion, label="media Generación", linestyle="--", color="blue", alpha=0.5)

# Demanda
plt.plot(df_central["Hora"], df_central["Demanda Neta MW"], label = "Demanda", color = "red")
plt.axhline(y=media_demanda, label="media Demanda", linestyle="--", color="red", alpha=0.5)

# Área generacion >= Demanda
plt.fill_between(df_central["Hora"], df_central["Generación Neta MW"], df_central["Demanda Neta MW"], where=(df_central["Generación Neta MW"] >= df_central["Demanda Neta MW"]), interpolate=True, color="lightgreen")
# Área generacion < Demanda
plt.fill_between(df_central["Hora"], df_central["Generación Neta MW"], df_central["Demanda Neta MW"], where=(df_central["Generación Neta MW"] < df_central["Demanda Neta MW"]), interpolate=True, color="yellow", alpha = .45)

# Diferencias
plt.scatter(df_central["Hora"], puntos_medios , label = "Diferencia", marker = "x", s = 20, alpha = 0.8, color = "purple")
for i, valor in enumerate(puntos_medios):
    plt.text(df_central["Hora"].iloc[i], valor, f"{valor}")

# Texto
#plt.text(0, min_generacion-2500 ,f"Fecha: {dia}\nDemanda MW\n* Max: {max_demanda}\n* Min: {min_demanda}\n* Media: {media_demanda}\nConsumo MW\n* Max: {max_generacion}\n* Min: {min_generacion}\n* Media: {media_generacion}")

tabla_info = f"""
Fecha: {dia}\n

{'':<15}Demanda MW{'':<15}Consumo MW{'':<15}
{'-'*66:<15}
{'Max   :':<15}{max_demanda:<29}{max_generacion:<15}
{'Min    :':<16}{min_demanda:<29}{min_generacion:<15}
{'Media:':<14}{media_demanda:<29}{media_generacion:<15}
"""
plt.text(0, min_generacion - 2500, tabla_info, fontsize=10)


plt.title("Demanda Sistema Eléctrico Nacional", fontsize = 20)
plt.xlabel("Hora", fontsize = 15)
plt.ylabel("Demanda MW", fontsize = 15)

plt.legend(loc = "upper left")
plt.show()

# %%
if df_central["Hora"].iloc[-1] == 00:
    plt.savefig("../imagenes_cv/"+ fecha + hora + ".csv")


