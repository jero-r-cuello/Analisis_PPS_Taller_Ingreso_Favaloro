#%%
import nltk
from nltk.corpus import stopwords
import re
from bertopic import BERTopic
import pandas as pd
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# Descargar stopwords en español
nltk.download('stopwords')
stop_words = set(stopwords.words('spanish'))
stop_words.update(["carrera", "facultad", "universidad", "muchas", "llevo", "brinda"])

def clean_text(text):
    """Limpia el texto eliminando stopwords, signos de puntuación y caracteres especiales"""
    text = text.lower()  # Convertir a minúsculas
    text = re.sub(r'\d+', '', text)  # Eliminar números
    text = re.sub(r'[^\w\s]', '', text)  # Eliminar signos de puntuación
    words = text.split()
    words = [word for word in words if word not in stop_words]  # Eliminar stopwords
    return ' '.join(words)

# dfs con respuestas
rtas_total = pd.read_csv("Facu/Quinto año/PPS OVO/analisis/Evaluación_ Primeros pasos en la vida universitaria (COMISIÓN 1) (Responses) - Form Responses 1.csv")
"""df_com2 = pd.read_csv("Evaluación_ Primeros pasos en la vida universitaria (COMISIÓN 2) (Responses) - Form Responses 1.csv")
df_comv = pd.read_csv("Evaluación_ Primeros pasos en la vida universitaria (VESPERTINO) (Responses) - Form Responses 1.csv")

rtas_total = pd.concat([df_com1,df_com2,df_comv], axis=0)
"""
#%%
docs = rtas_total["¿Qué ideas te llevas de este taller?"]

docs_cleaned = [clean_text(doc) for doc in docs]

# Crear el modelo y extraer tópicos
topic_model = BERTopic()
topics, probs = topic_model.fit_transform(docs_cleaned)

print(topic_model.get_topic_info())
# %%
topic_info = topic_model.get_topic_info()
topic_words = {
    row["Topic"]: row["Representation"] for _, row in topic_info.iterrows()
}



# Tokenización simple (puedes usar spaCy/NLTK si quieres algo más avanzado)
word_counts = Counter(" ".join(docs_cleaned).lower().split())

# Crear DataFrame con las palabras clave y sus frecuencias
topic_word_counts = []
for topic, words in topic_words.items():
    for word in words:
        topic_word_counts.append({"Tópico": topic, "Palabra": word, "Frecuencia": word_counts.get(word, 0)})

df = pd.DataFrame(topic_word_counts)

# %%

for topic, words in topic_words.items():
    word_freq = {word: word_counts.get(word, 0) for word in words}
    
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate_from_frequencies(word_freq)
    
    plt.figure(figsize=(8, 4))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title(f"Tópico {topic}")
    plt.show()

# %%
