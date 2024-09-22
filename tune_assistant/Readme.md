# RAG Agent in Python for Internet Scraping using Supabase

This repository contains the code for setting up a Retrieval-Augmented Generation (RAG) agent using Python, aimed at scraping data from the internet and using it to enhance response generation. The system integrates several technologies including TuneStudio with the llama 3 model, OpenAI for generating embeddings, and Supabase for data storage.

## Features

- Scrape web content using BeautifulSoup
- Extract and clean text data from websites
- Generate embeddings using OpenAI API
- Store and query data in Supabase
- Serve results through a FastAPI server

## Installation

### Dependencies

To install the required dependencies, clone the repository and run:

```bash
pip install -r requirements.txt
```

### Environment Setup

You must provide the following environment variables. Create a `.env` file in your project's root directory with your keys:

```plaintext
TUNE_API_KEY={your_tune_api_key}
SUPABASE_URL={your_supabase_url}
SUPABASE_KEY={your_supabase_key}
OPENAI_API_KEY={your_openai_api_key}
```

Keys can be obtained from:

- Tune API key: [Tune Studio](https://studio.tune.app/profile)
- Supabase URL and Key: [Supabase Project Settings](https://supabase.com/)
- OpenAI API Key: [OpenAI Platform](https://platform.openai.com/)

## Database Setup

Use the following SQL commands in Supabase to set up your database:

```sql
-- Create vector extension
create extension vector;
-- Create documents table
create table documents (
  id bigserial primary key,
  content text,
  embedding vector(1536),
  url text,
  title text
);

-- Create function for matching documents
create or replace function match_documents (
  query_embedding vector(1536),
  match_threshold float,
  match_count int
)
returns table (
  id bigint,
  content text,
  url text,
  title text,
  similarity float
)
language sql stable
as $$
  select
    documents.id,
    documents.content,
    documents.url,
    documents.title,
    1 - (documents.embedding <=> query_embedding) as similarity
  from documents
  where documents.embedding <=> query_embedding < 1 - match_threshold
  order by documents.embedding <=> query_embedding
  limit match_count;
$$;
```

## Running the Server

To start up the FastAPI server, navigate to the project's root directory and execute:

```bash
python main.py
```

The server will be available at `http://localhost:8000`.

## API Endpoints

The server provides the following endpoints:

### POST `/add_documents`

- Input: JSON payload with the URL of the website to extract data from.
- Functionality: Processes the website to extract text, generates embeddings, and stores the data in Supabase.
- Example curl:

```bash
curl -X POST http://localhost:8000/add_documents \
     -H "Content-Type: application/json" \
     -d '{"url":"http://example.com"}'
```

### POST `/prompt`

- Input: JSON payload with a user query string.
- Functionality: Queries the database based on embeddings similarity and returns relevant documents.
- Example curl:

```bash
curl -X POST http://localhost:8000/prompt \
     -H "Content-Type: application/json" \
     -d '{"query":"example query"}'
```

## Repository Structure

- `main.py`: FastAPI server setup and endpoints.
- `utils.py`: Utility functions including data scraping, cleaning, embedding generation, and database interaction.

For more details, refer to the inline comments in the code.

Keep Tuning!
