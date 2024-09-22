import requests
import numpy as np
from langchain.embeddings import OllamaEmbeddings
from langchain.vectorstores import Chroma

embedding_model = OllamaEmbeddings(model="nomic-embed-text:latest")
vector_store = Chroma(embedding_function=embedding_model)

# def load_email_data(file_path):
#     with open(file_path, 'r') as file:
#         return json.load(file)

# emails = load_email_data('data/gmail/test.json')

# for email in emails:
#     id = email['id']  # Use the existing ID from mbox
#     content = email['body']  # Assuming 'body' contains the main content
#     subject = email['subject']
#     fromM = email['from']
#     to = email['to']
#     date = email['date']
#     cc = email['cc']
#     bcc = email['bcc']
#     # Create embedding
#     embedding = embedding_model.embed_documents([content])
#     # metadata = {'id':id,'subject':subject,'from':fromM,'to':to,'date':date,'cc':cc,'bcc':bcc}
#     metadata = {'id':id,'subject':subject,'from':fromM}
#     # filtered_metadata = filter_complex_metadata(metadata)

    
#     # Store in vector store
#     vector_store.add_texts([content], embedding=[embedding], metadatas=[metadata])


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
    results = vector_store.similarity_search(query_embedding[0], k=10)  # Fetch top 5 results
    return results


# user_query = "Emails from HDFC"

# relevant_emails = retrieve_relevant_emails(user_query)

# Print results
# for doc in relevant_emails:
#     print("["+doc.metadata['from']+"]"+doc.metadata['subject'])
    
    # print(f"Email ID: {doc.metadata['id']}, Content: {doc.page_content}")
