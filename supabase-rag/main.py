import time
from fastapi import FastAPI, Request
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from fastapi.responses import StreamingResponse

# file we wrote
from utils import extract_website_data, get_response_tunestudio, search_documents

load_dotenv()  # Loads environment variables from .env file
app = FastAPI()


class DocumentBody(BaseModel):
    url: str = Field(..., title="URL of the website to extract data from")


class SearchBody(BaseModel):
    query: str


@app.post("/add_documents")
def read_root(document: DocumentBody):
    url = document.url
    print("URL:", url)
    start_time = time.time()
    urls = extract_website_data(url, start_time)
    return {"urls_processed": len(urls), "time_taken": time.time() - start_time}


@app.post("/prompt")
def resolve_prompt(prompt: SearchBody):
    prompt = prompt.query
    search = search_documents(prompt)
    return StreamingResponse(
        get_response_tunestudio(prompt, search.data), media_type="text/event-stream"
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
