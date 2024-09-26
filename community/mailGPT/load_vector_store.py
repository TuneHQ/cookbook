import json
from langchain.embeddings import OllamaEmbeddings
from langchain.vectorstores import Chroma

embedding_model = OllamaEmbeddings(model="nomic-embed-text:latest")
vector_store = Chroma(embedding_function=embedding_model)

def load_email_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def store_email_embeddings_to_vector_store(emails):
    for email in emails:
        id = email['id']  
        content = email['body']
        subject = email['subject']
        fromM = email['from']
        to = email['to']
        date = email['date']
        cc = email['cc']
        bcc = email['bcc']
        
        embedding = embedding_model.embed_documents([content])
        
        metadata = {'id':id,'subject':subject,'from':fromM}
        vector_store.add_texts([content], embedding=[embedding], metadatas=[metadata])