import streamlit as st
import requests

# Set FastAPI backend URL
FASTAPI_URL = "http://localhost:8000"  # Change this to the actual server URL if deployed

st.title("Website Ingestion and Querying")

# Section for website ingestion
st.header("Ingest Website Content")
url = st.text_input("Enter the URL of the website")

if st.button("Ingest Website"):
    if url:
        response = requests.post(f"{FASTAPI_URL}/add_documents", json={"url": url})
        if response.status_code == 200:
            result = response.json()
            st.success(f"Website processed. URLs processed: {result['urls_processed']}, Time taken: {result['time_taken']} seconds")
        else:
            st.error(f"Failed to process the website. Error: {response.text}")
    else:
        st.warning("Please enter a URL.")

# Section for querying the ingested documents
st.header("Query Ingested Data")
query = st.text_input("Enter your query")

if st.button("Search"):
    if query:
        response = requests.post(f"{FASTAPI_URL}/prompt", json={"query": query}, stream=True)
        if response.status_code == 200:
            for chunk in response.iter_content(chunk_size=None):
                if chunk:
                    st.write(chunk.decode('utf-8'))
        else:
            st.error(f"Failed to get response. Error: {response.text}")
    else:
        st.warning("Please enter a query.")
