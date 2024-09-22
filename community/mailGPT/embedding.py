import json
import requests
import numpy as np

emails_with_embeddings = {}
threshold = 0.4

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
    a = np.array(a)  # Ensure a is a numpy array
    b = np.array(b)  # Ensure b is a numpy array
    return np.dot(a, b.T) / (np.linalg.norm(a) * np.linalg.norm(b))

def retrieve_relevant_emails(query, emails_with_embeddings):
    query_embedding = get_embeddings(query)  # Assuming this function returns a numpy array
    if not query_embedding:
        return []  # Handle cases where embeddings could not be fetched
    relevant_emails = []
    for email in emails_with_embeddings:
        email_embedding = email['embedding']  # Ensure this is a numpy array
        if not email_embedding:
            continue  # Skip emails where embedding could not be fetched
        sim = cosine_similarity(query_embedding['embeddings'], email_embedding['embeddings'])
        if sim > threshold:  # Define a threshold for relevance
            email['similarity'] = sim  # Store the similarity score with the email
            relevant_emails.append(email)

    # Sort emails by similarity score in descending order and return top 10
    relevant_emails.sort(key=lambda x: x['similarity'], reverse=True)
    return relevant_emails[:10]

# emails = load_email_data('data/gmail/test.json')
# emails_with_embeddings = prepare_email_embeddings(emails)

# query = "top linkedin emails"
# relevant_emails = retrieve_relevant_emails(query, emails_with_embeddings)

# for relevant_email in relevant_emails:
#     print(f"Subject: {relevant_email['subject']}")
#     print(f"From: {relevant_email['from']}")
#     print(f"Similarity: {relevant_email['similarity']}\n")
