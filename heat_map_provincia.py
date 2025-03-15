#%%
# Reimportar librerías después del reset del entorno
import geopandas as gpd
import pandas as pd
import matplotlib
%matplotlib qt
import matplotlib.pyplot as plt
import contextily as ctx
import numpy as np
import matplotlib.patheffects as path_effects

import zipfile
import os

#%%
# Cargar el shapefile del nivel 2 (Departamentos/Municipios) para toda Argentina
shapefile_path = f"C:/Users/54113/OneDrive/Escritorio/Facu/Quinto año/PPS OVO/analisis/gadm41_ARG_shp_extracted/gadm41_ARG_2.shp"
gdf_ba = gpd.read_file(shapefile_path)

# Filtrar solo la Provincia de Buenos Aires y CABA
gdf_ba = gdf_ba[gdf_ba["NAME_1"].isin(["Buenos Aires", "Ciudad Autónoma de Buenos Aires"])]

# Ver las primeras filas para confirmar la estructura
gdf_ba.head()
# Diccionario para normalizar nombres de partidos/municipios en las respuestas
mapeo_ba = {
    "caba": "Ciudad Autónoma de Buenos Aires",
    "capital federal": "Ciudad Autónoma de Buenos Aires",
    "c.a.b.a": "Ciudad Autónoma de Buenos Aires",
    "Belgrano": "Ciudad Autónoma de Buenos Aires",
    "palermo": "Ciudad Autónoma de Buenos Aires",
    "almagro": "Ciudad Autónoma de Buenos Aires",
    "monserrat": "Ciudad Autónoma de Buenos Aires",
    "san cristóbal": "Ciudad Autónoma de Buenos Aires",
    "balvanera": "Ciudad Autónoma de Buenos Aires",
    "recoleta": "Ciudad Autónoma de Buenos Aires",
    "liniers": "Ciudad Autónoma de Buenos Aires",
    "villa crespo": "Ciudad Autónoma de Buenos Aires",
    "devoto": "Ciudad Autónoma de Buenos Aires",
    "saavedra": "Ciudad Autónoma de Buenos Aires",
    "villa urquiza": "Ciudad Autónoma de Buenos Aires",
    "villa del parque": "Ciudad Autónoma de Buenos Aires",
    "caballito": "Ciudad Autónoma de Buenos Aires",
    "coghlan": "Ciudad Autónoma de Buenos Aires",
    "flores": "Ciudad Autónoma de Buenos Aires",
    "parque patricios": "Ciudad Autónoma de Buenos Aires",
    "avellaneda": "Avellaneda",
    "Lanús": "Lanús",
    "lomas de zamora": "Lomas de Zamora",
    "Vicente López": "Vicente López",
    "San Isidro": "San Isidro",
    "Escobar": "Escobar",
    "la plata": "La Plata",
    "san martín": "General San Martín",
    "Olivos": "Vicente López",
    "temperley": "Lomas de Zamora",
    "Banfield": "Lomas de Zamora",
    "caseros": "Tres de Febrero",
    "Martínez": "San Isidro",
    "Berazategui": "Berazategui",
    "Florencio Varela": "Florencio Varela"
}

# Procesar los datos de residencia y agrupar por partido/municipio
df_residencias_ba = pd.Series({
"CABA":18,
"Florencio Varela":2,
"Belgrano":2,
"Lanús":4,
"San Cristóbal":1,
"Berazategui":1,
"Monserrat":1,
"Almagro":2,
"Palermo":1,
"Coghlan":1,
"Banfield":2,
"San Isidro":3,
"Escobar":2,
"Olivos":3,
"Balvanera":3,
"Martínez":2
}
).reset_index()

df_residencias_ba.columns = ["PARTIDO_ORIGINAL", "POBLACION"]
df_residencias_ba["PARTIDO"] = df_residencias_ba["PARTIDO_ORIGINAL"].map(mapeo_ba)

# Unir los datos de población con los municipios/partidos
gdf_ba = gdf_ba.merge(df_residencias_ba, left_on="NAME_2", right_on="PARTIDO", how="left")

# Crear la figura y los ejes
fig, ax = plt.subplots(figsize=(12, 12))

# Dibujar TODOS los partidos/municipios en blanco (para que aparezcan aunque no tengan datos)
gdf_ba.plot(color="white", linewidth=1, edgecolor="black", ax=ax)

# Dibujar SOLO los que tienen datos de residencia, usando una escala de color
gdf_ba.dropna(subset=["POBLACION"]).plot(
    column="POBLACION",
    cmap="YlOrRd",  # Escala de colores de amarillo a rojo
    linewidth=1,
    edgecolor="black",
    ax=ax,
    legend=False
)

# Agregar nombres de los partidos con borde negro y relleno blanco
for idx, row in gdf_ba.iterrows():
    if pd.notna(row["POBLACION"]):
        centroid = row["geometry"].centroid
        text = ax.text(centroid.x, centroid.y, row["NAME_2"], fontsize=8, 
                       ha="center", va="center", color="white", fontweight="bold")

        # Aplicar borde negro al texto
        text.set_path_effects([
            path_effects.Stroke(linewidth=2, foreground="black"),  # Borde negro
            path_effects.Normal()
        ])

# Agregar mapa base para mejorar apariencia
ctx.add_basemap(ax, source=ctx.providers.CartoDB.Positron, zoom=10, crs=gdf_ba.crs)

# Quitar ejes y bordes para que sea más limpio
ax.set_axis_off()

# Mostrar el mapa
plt.show()


# %%
