import os
os.kill(os.getpid(), 9)

import csv
import openai
from llama_index.core import VectorStoreIndex # Import directly from llama_index
from llama_index.core import Document
openai.api_key = 'sk-U7ti37t3osaeWme7m88923xFY2UMGVQLkeydTAywi3xI7TOP'
openai.base_url = "https://api.chatanywhere.tech/v1"

!git clone https://github.com/PacktPublishing/Python-Natural-Language-Processing-Cookbook-Second-Edition.git

with open('/content/Python-Natural-Language-Processing-Cookbook-Second-Edition/data/IMDB-Movie-Data.csv') as f:
  reader = csv.reader(f)
  data = list(reader)
  movies = data[1:]

documents = []
for movie in movies[0:10]:
    doc_id = movie[0]
    title = movie[1]
    genres = movie[2].split(",")
    description = movie[3]
    director = movie[4]
    actors = movie[5].split(",")
    year = movie[6]
    duration = movie[7]
    rating = movie[8]
    revenue = movie[10]
    document = Document(
        text=description,
        metadata={
            "title": title,
            "genres": genres,
            "director": director,
            "actors": actors,
            "year": year,
            "duration": duration,
            "rating": rating,
            "revenue": revenue
        }
    )
    print(document)
    documents.append(document)
index = VectorStoreIndex.from_documents(documents)

query_engine = index.as_query_engine()
response = query_engine.query("""Which movies talk about something gigantic?""")
print(response.response)