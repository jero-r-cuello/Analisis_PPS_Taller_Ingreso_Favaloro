# Análisis de Datos - Evaluación Taller "Primeros Pasos en la Vida Universitaria"

## Descripción

Este repositorio contiene los scripts utilizados para el análisis de datos de la evaluación del taller "Primeros Pasos en la Vida Universitaria", llevado a cabo en la Universidad Favaloro.
Los análisis incluyen la caracterización de la población participante, el análisis de sentimiento de los comentarios de los estudiantes, y la identificación de temas clave en las respuestas abiertas.

## Archivos y Funcionalidades

### 1. `analisis_de_topicos.py`

- Utiliza el modelo **BERTopic** para identificar tópicos en las respuestas de los estudiantes a la pregunta "¿Qué ideas te llevas de este taller?".
- Filtra y limpia el texto eliminando stopwords y caracteres especiales.
- Genera visualizaciones de nubes de palabras por cada tópico identificado.

### 2. `sentiment_analysis_LLM.py`

- Aplica un modelo de **transformers** (FLAN-T5) para clasificar el sentimiento de los comentarios de los participantes.
- Evalúa la proporción de respuestas con sentimiento positivo y negativo.
- Genera gráficos de distribución de sentimientos.

### 3. `heat_map_CABA.py`

- Procesa y visualiza la distribución geográfica de los participantes en la Ciudad Autónoma de Buenos Aires.
- Utiliza datos geoespaciales para generar un **mapa de calor** con los barrios donde residen los estudiantes.
- Agrega etiquetas con nombres de barrios para una mejor interpretación.

### 4. `heat_map_provincia.py`

- Similar al análisis de CABA, pero ampliado a la **Provincia de Buenos Aires**.
- Normaliza nombres de partidos/municipios para un análisis más preciso.
- Genera un **mapa de calor** con la distribución de estudiantes en distintos municipios.

## Datos Utilizados

Los análisis se realizaron con datos obtenidos de la **encuesta de evaluación del taller**. Estos datos incluyen:

- **Información de residencia** de los estudiantes.
- **Comentarios abiertos** sobre su experiencia en el taller.
- **Percepción general del taller** y su impacto en la transición universitaria.
