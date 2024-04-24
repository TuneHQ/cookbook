import time
from typing import Union
from fastapi import FastAPI
from utils import extract_website_data

app = FastAPI()


@app.get("/")
def read_root():
    url = "https://js.langchain.com/docs/get_started/introduction/"
    start_time = time.time()
    urls = extract_website_data(url,start_time)
    print("Extracted URLs:", urls)

    return {"urls": urls, "time_taken": time.time() - start_time}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}