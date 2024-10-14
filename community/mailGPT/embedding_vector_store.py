import requests
import numpy as np
from langchain.embeddings import OllamaEmbeddings
from langchain.vectorstores import Chroma

embedding_model = OllamaEmbeddings(model="nomic-embed-text:latest")
vector_store = Chroma(embedding_function=embedding_model)

def get_embeddings(text):
    url = "http://localhost:11434/api/embed"
    response = requests.post(url, json={"model":"nomic-embed-text:latest","input": text})
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching embeddings: {response.status_code} - {response.text}")
        return None

def prepare_email_embeddings(emails):
    for email in emails:
        email['embedding'] = get_embeddings(email['body'])
    return emails

def retrieve_relevant_emails(query):
    query_embedding = embedding_model.embed_documents([query])
    results = vector_store.similarity_search(query_embedding[0], k=10)
    return results
