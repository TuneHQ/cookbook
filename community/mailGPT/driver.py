import json
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain_community.chat_models import ChatOllama

# Load the email data
with open('data/gmail/all_adv_with_id.json', 'r') as f:
    email_data = json.load(f)

# Step 1: Create embeddings using Ollama
def create_embeddings(emails):
    llm = ChatOllama(model="gemma2:9b",
                 keep_alive="3h", 
                 max_tokens=5012,  
                 temperature=0)
    # llm = Ollama(model_name='nomic-embed-text')  # Specify your embedding model
    embeddings = []
    
    for email in emails:
        # Call Ollama to generate embeddings for the email body
        embedding = llm(email['body'])
        embeddings.append(embedding)
    
    return embeddings

# Step 2: Create a FAISS vector store
email_texts = [email['body'] for email in email_data]
email_ids = [email['id'] for email in email_data]
embeddings = create_embeddings(email_data)

faiss_index = FAISS.from_embeddings(embeddings, email_ids)

# Step 3: Setup the retrieval function
def retrieve_relevant_emails(query, top_k=5):
    query_embedding = llm(query)  # Call Ollama for the query embedding
    D, I = faiss_index.search(query_embedding, top_k)
    relevant_emails = [email_data[i] for i in I[0]]
    return relevant_emails

# Step 4: Call Ollama API to generate responses
def get_llm_response(relevant_emails, user_query):
    # Create the prompt
    prompt = PromptTemplate(
        input_variables=["emails", "query"],
        template="Based on the following emails: {emails}, please answer this query: {query}"
    )

    emails_content = "\n\n".join(email['body'] for email in relevant_emails)
    formatted_prompt = prompt.format(emails=emails_content, query=user_query)

    # Call Ollama for the response
    llm_response = llm(formatted_prompt)
    return llm_response

# Example usage
user_query = "What are the latest offers in the emails?"
relevant_emails = retrieve_relevant_emails(user_query)
print("relevant_emails: ----->"+relevant_emails)
# response = get_llm_response(relevant_emails, user_query)

# print("Response from Ollama:", response)
