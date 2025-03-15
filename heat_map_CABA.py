# %%
# Reimportar librerías después del reset del entorno
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import contextily as ctx
import numpy as np
import matplotlib.patheffects as path_effects

# Cargar los barrios de CABA (GeoJSON)
url = "https://cdn.buenosaires.gob.ar/datosabiertos/datasets/barrios/barrios.geojson"
gdf_barrios = gpd.read_file(url)

# Diccionario para normalizar nombres de barrios en las respuestas
mapeo_barrios = {
    "Belgrano": "BELGRANO",
    "Palermo": "PALERMO",
    "Almagro": "ALMAGRO",
    "Monserrat": "MONSERRAT",
    "San Cristóbal": "SAN CRISTOBAL",
    "Balvanera": "BALVANERA",
    "Recoleta": "RECOLETA",
    "Liniers": "LINIERS",
    "Villa crespo": "VILLA CRESPO",
    "Devoto": "VILLA DEVOTO",
    "Saavedra": "SAAVEDRA",
    "Villa Urquiza": "VILLA URQUIZA",
    "Villa del Parque": "VILLA DEL PARQUE",
    "Caballito": "CABALLITO",
    "Coghlan": "COGHLAN",
    "Flores": "FLORES",
    "Parque Patricios": "PARQUE PATRICIOS"
}

# Procesar los datos de residencia y agrupar por barrio
df_residencias = pd.Series({
"CABA":18,
"Florencio Varela":2,
"Belgrano":2,
"Lanús":4,
"San Cristóbal":1,
"Berazategui":1,
"Monserrat":1,
"Almagro":2,
"Palermo":1,
"Vicente López":2,
"Coghlan":1,
"Banfield":2,
"San Isidro":1,
"Escobar":2,
"Olivos":1,
"Balvanera":1,
"Martínez":1
}
).reset_index()


df_residencias.columns = ["BARRIO_ORIGINAL", "POBLACION"]
df_residencias["BARRIO"] = df_residencias["BARRIO_ORIGINAL"].map(mapeo_barrios)

# Unir los datos de población con los barrios de CABA
gdf_barrios = gdf_barrios.merge(df_residencias, on="BARRIO", how="left")

# Crear la figura y los ejes
fig, ax = plt.subplots(figsize=(10, 10))

# Dibujar TODOS los barrios en blanco (para que aparezcan aunque no tengan datos)
gdf_barrios.plot(color="white", linewidth=1, edgecolor="black", ax=ax)

# Dibujar SOLO los barrios con datos de residencia, usando una escala de color
gdf_barrios.dropna(subset=["POBLACION"]).plot(
    column="POBLACION",
    cmap="YlOrRd",  # Escala de colores de amarillo a rojo
    linewidth=1,
    edgecolor="black",
    ax=ax,
    legend=False
)

# Agregar nombres de los barrios con borde negro y relleno blanco
for idx, row in gdf_barrios.iterrows():
    if pd.notna(row["POBLACION"]):
        centroid = row["geometry"].centroid
        text = ax.text(centroid.x, centroid.y, row["BARRIO"], fontsize=8, 
                       ha="center", va="center", color="white", fontweight="bold")

        # Aplicar borde negro al texto
        text.set_path_effects([
            path_effects.Stroke(linewidth=2, foreground="black"),  # Borde negro
            path_effects.Normal()
        ])

# Agregar mapa base para mejorar apariencia
ctx.add_basemap(ax, source=ctx.providers.CartoDB.Positron, zoom=12, crs=gdf_barrios.crs)

# Quitar ejes y bordes para que sea más limpio
ax.set_axis_off()

# Mostrar el mapa
plt.show()

# %%
