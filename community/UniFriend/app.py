import streamlit as st
import os
from dotenv import load_dotenv
import tempfile

from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import PyPDFLoader
from langchain.docstore.document import Document
from langchain.indexes import VectorstoreIndexCreator
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings

import chromadb
from chromadb.utils import embedding_functions
import pandas as pd
import tabula
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv('TUNE_API_KEY')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# Initialize Streamlit app
st.set_page_config(page_title="UniFriend", layout="wide")
st.title("📄 UniFriend: PDF Chatbot for better Seat Selection")

# Function to extract text from PDF
def extract_text_from_pdf(file_path):
    loader = PyPDFLoader(file_path)
    pages = loader.load()
    return pages

# Function to extract tables from PDF
def extract_tables_from_pdf(file_path):
    try:
        tables = tabula.read_pdf(file_path, pages='all', multiple_tables=True)
        documents = []
        for idx, df in enumerate(tables):
            table_text = df.to_csv(index=False)
            doc = Document(
                page_content=table_text,
                metadata={"source": f"Table {idx+1}"}
            )
            documents.append(doc)
        return documents
    except Exception as e:
        st.warning(f"Could not extract tables: {e}")
        return []

# File uploaders
cutoff_pdf = st.file_uploader("Upload the Cutoff Marks PDF", type=["pdf"], key='cutoff')
scorecard_pdf = st.file_uploader("Upload the Scorecard PDF", type=["pdf"], key='scorecard')

if cutoff_pdf is not None and scorecard_pdf is not None:
    # Save uploaded files to temporary locations
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_cutoff_file:
        tmp_cutoff_file.write(cutoff_pdf.getvalue())
        tmp_cutoff_path = tmp_cutoff_file.name

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_scorecard_file:
        tmp_scorecard_file.write(scorecard_pdf.getvalue())
        tmp_scorecard_path = tmp_scorecard_file.name

    # Extract text and tables from PDFs
    st.info("Extracting text and tables from PDFs...")
    cutoff_documents = extract_text_from_pdf(tmp_cutoff_path) + extract_tables_from_pdf(tmp_cutoff_path)
    scorecard_documents = extract_text_from_pdf(tmp_scorecard_path) + extract_tables_from_pdf(tmp_scorecard_path)

    # Combine documents
    documents = cutoff_documents + scorecard_documents

    # Split text for embeddings
    st.info("Splitting text into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    split_docs = text_splitter.split_documents(documents)

    # Generate embeddings and store in ChromaDB
    st.info("Generating embeddings and storing in vector database...")
    embeddings = GoogleGenerativeAIEmbeddings(model='models/embedding-001', google_api_key=GOOGLE_API_KEY)

    persist_directory = './chroma_db'
    vectordb = Chroma.from_documents(
        documents=split_docs,
        embedding=embeddings,
        persist_directory=persist_directory
    )

    st.success("Embeddings generated and stored in ChromaDB!")

    # Initialize chat history
    if 'history' not in st.session_state:
        st.session_state['history'] = []

    # Chat interface
    st.header("🗨️ Chat with your PDFs")
    user_question = st.text_input("Ask a question about the PDFs:", key='input')

    if user_question:
        # Retrieve relevant documents
        docs = vectordb.similarity_search(user_question, k=4)

        # Combine relevant documents
        context = "\n\n".join([doc.page_content for doc in docs])

        # Initialize chat model
        chat_model = ChatOpenAI(
            openai_api_key=OPENAI_API_KEY,
            openai_api_base="https://proxy.tune.app/",
            model_name="kaushikaakash04/tune-blob"
        )

        # Generate response
        prompt = f"You are a helpful assistant analyzing PDF documents.\n\nContext:\n{context}\n\nQuestion:\n{user_question}\n\nAnswer:"
        try:
            response = chat_model.predict(prompt)
            st.session_state['history'].append((user_question, response))
            st.write("**Answer:**", response)
        except Exception as e:
            st.error(f"Error generating response: {e}")

    # Display chat history
    if st.session_state['history']:
        st.subheader("Chat History")
        for i, (q, a) in enumerate(st.session_state['history']):
            st.write(f"**Q{i+1}:** {q}")
            st.write(f"**A{i+1}:** {a}")
else:
    st.info("Please upload both the Cutoff Marks PDF and the Scorecard PDF to proceed.")

# Clean up temporary files
if cutoff_pdf is not None:
    os.remove(tmp_cutoff_path)
if scorecard_pdf is not None:
    os.remove(tmp_scorecard_path)
