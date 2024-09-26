import json
import requests
import numpy as np
import configuration

emails_with_embeddings = {}
threshold = configuration.EMBEDDING_COSINE_SIMILARITY_THRESHOLD

def load_email_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

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
        # email['embedding'] = get_embeddings(email['body']) ## prepare embedding on body
        email['embedding'] = get_embeddings(email['subject']) ## prepare embedding on subject
    return emails

def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b.T) / (np.linalg.norm(a) * np.linalg.norm(b))

def retrieve_relevant_emails(query, emails_with_embeddings):
    query_embedding = get_embeddings(query)
    if not query_embedding:
        return []
    relevant_emails = []
    for email in emails_with_embeddings:
        email_embedding = email['embedding']
        if not email_embedding:
            continue  # Skip emails where embedding could not be fetched
        sim = cosine_similarity(query_embedding['embeddings'], email_embedding['embeddings'])
        if sim > threshold:  # Define a threshold for relevance
            email['similarity'] = sim  # Store the similarity score with the email
            relevant_emails.append(email)

    relevant_emails.sort(key=lambda x: x['similarity'], reverse=True)
    return relevant_emails[:configuration.NUMBER_OF_EMAILS_FOR_RAG]