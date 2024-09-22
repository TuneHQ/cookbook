from dotenv import load_dotenv
import os
import requests
import fire

# Load environment variables
load_dotenv()
NOTION_KEY = os.getenv("NOTION_KEY")
TUNEAI_TOKEN = os.getenv("TUNEAI_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_KEY")

# Headers for API requests
notion_headers = {
    "Authorization": f"Bearer {NOTION_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}


# Call Proximity LLM to generate content
def call_llm(messages, model="rohan/mixtral-8x7b-inst-v0-1-32k"):
    url = "https://proxy.tune.app/chat/completions"
    headers = {
        "Authorization": TUNEAI_TOKEN,
        "Content-Type": "application/json",
    }
    data = {
        "temperature": 0.8,
        "messages": messages,
        "model": model,
        "stream": False,
        "frequency_penalty": 0,
        "max_tokens": 500,
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"].strip()


# Scraping article structure based on topic
def gen_article(topic, model):
    messages = [
        {
            "role": "system",
            "content": "You are an GEN AI expert. Your task is to generate an article on the given topic in a structured format: Introduction, Key Points, Conclusion."
        },
        {"role": "user", "content": f"Generate an article for the topic: {topic}"}
    ]
    return call_llm(messages, model)


# Generate title for article
def gen_article_title(topic, model):
    messages = [
        {
            "role": "system",
            "content": "Generate a concise and engaging title based on the topic."
        },
        {"role": "user", "content": topic}
    ]
    return call_llm(messages, model)


# Scrape cover image for the article
def get_cover_image(article_title):
    url = "https://google.serper.dev/images"
    serper_headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json",
    }
    data = {"q": article_title}
    response = requests.post(url, headers=serper_headers, json=data)
    response_data = response.json()
    return response_data["images"][0]["imageUrl"]


# Main function to generate and store the article
def main(topic, page_id, model):
    # Generate the article structure
    article_title = gen_article_title(topic, model)
    article_body = gen_article(topic, model)

    # Get cover image for article
    cover_image = get_cover_image(article_title)

    # Create the article page in Notion
    data = {
        "parent": {"page_id": page_id},
        "properties": {"title": [{"text": {"content": article_title}}]},
        "cover": {"external": {"url": cover_image}},
    }

    response = requests.post(
        "https://api.notion.com/v1/pages", headers=notion_headers, json=data
    )
    page_data = response.json()

    # Add article content
    article_content = {
        "children": [
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": "Introduction"}}]
                }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": article_body}}]
                }
            }
        ]
    }

    # Append content to the Notion page
    requests.patch(
        f"https://api.notion.com/v1/blocks/{page_data['id']}/children",
        headers=notion_headers,
        json=article_content
    )


if __name__ == "__main__":
    fire.Fire(main)