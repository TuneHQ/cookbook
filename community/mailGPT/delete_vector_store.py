from langchain.embeddings import OllamaEmbeddings
from langchain.vectorstores import Chroma

embedding_model = OllamaEmbeddings(model="nomic-embed-text:latest")
vector_store = Chroma(embedding_function=embedding_model)

vector_store.delete_collection()