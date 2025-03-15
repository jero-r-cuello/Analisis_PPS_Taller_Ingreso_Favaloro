# %%
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Modelo LLM
model_name = "google/flan-t5-large"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

text2text_generator = pipeline(
    "text2text-generation",
    model=model,
    tokenizer=tokenizer
)

# Función para predecir sentimiento
def predict_sentiment(sentence, label_space=["negative", "positive"]):
    """
    Dado un texto, asigna un sentimiento basado en las etiquetas definidas.
    """    
    prompt = (
        f"Please perform Sentiment Classification task. "
        f"Given the sentence \"{sentence}\", assign a sentiment label from {label_space}. "
        f"Return label only without any other text."
    )
    
    # Generar salida del modelo
    outputs = text2text_generator(prompt)
    generated_text = outputs[0]["generated_text"].strip()
    return generated_text

# Cargar datos
df = pd.read_csv("Facu/Quinto año/PPS OVO/analisis/Evaluación_ Primeros pasos en la vida universitaria (COMISIÓN 1) (Responses) - Form Responses 1.csv")

docs = df["¿Qué ideas te llevas de este taller?"].dropna()

# Aplicar análisis de sentimiento usando el modelo LLM
df_sentiment = pd.DataFrame({
    "Texto": docs,
    "Sentimiento": [predict_sentiment(doc) for doc in docs]
})

# Gráfico de distribución del sentimiento
plt.figure(figsize=(8, 5))
sns.histplot(df_sentiment['Sentimiento'], bins=3, kde=False, palette="coolwarm")
plt.xlabel("Sentimiento")
plt.ylabel("Cantidad de Reportes")
plt.title("Distribución del Sentimiento en los Reportes")
plt.show()

# Gráfico de barras de cantidad de reportes por sentimiento
plt.figure(figsize=(8, 5))
sns.countplot(x=df_sentiment['Sentimiento'], palette="coolwarm")
plt.xlabel("Sentimiento")
plt.ylabel("Cantidad de Reportes")
plt.title("Cantidad de Reportes por Sentimiento")
plt.show()

# %%
