import os
import time
from typing import Union
from fastapi import FastAPI, Request
from utils import extract_website_data, search_documents
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()  # Loads environment variables from .env file
app = FastAPI()

class DocumentBody(BaseModel):
    url : str = Field(..., title="URL of the website to extract data from")

@app.post("/add_documents")
def read_root( document: DocumentBody):
    url = document.url
    print("URL:", url)
    start_time = time.time()
    urls = extract_website_data(url,start_time)

    return {"urls_processed": len(urls), "time_taken": time.time() - start_time}


@app.get("/prompt")
def resolve_prompt(request: Request):
    params = request.query_params
    prompt = params.get("query")
    search = search_documents(prompt)
    print("Prompt:", search)
    