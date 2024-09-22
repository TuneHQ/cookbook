import feedparser
import requests
from bs4 import BeautifulSoup
from transformers import pipeline
import json

# Configuration
RSS_FEED_URL = "https://example.com/rss-feed-url"
TUNE_STUDIO_API_URL = "https://api.tunestudio.com/v1/send-message"
TUNE_STUDIO_API_KEY = "your_tune_studio_api_key"
WHATSAPP_CHANNEL_ID = "your_whatsapp_channel_id"

def fetch_rss_feed(url):
    """Fetch and parse the RSS feed."""
    feed = feedparser.parse(url)
    return feed.entries

def extract_article_content(url):
    """Extract the main content of an article."""
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    # This is a simple extraction. You might need to adjust it based on the website structure.
    article = soup.find('article') or soup.find('div', class_='content')
    return article.get_text() if article else ""

def summarize_text(text):
    """Summarize the given text using a pre-trained model."""
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    summary = summarizer(text, max_length=150, min_length=50, do_sample=False)
    return summary[0]['summary_text']

def send_to_tune_studio(message):
    """Send the summarized message to Tune Studio."""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {TUNE_STUDIO_API_KEY}"
    }
    payload = {
        "channel_id": WHATSAPP_CHANNEL_ID,
        "message": message
    }
    response = requests.post(TUNE_STUDIO_API_URL, headers=headers, data=json.dumps(payload))
    return response.status_code == 200

def main():
    # Fetch RSS feed
    entries = fetch_rss_feed(RSS_FEED_URL)
    
    for entry in entries[:5]:  # Process the first 5 entries
        # Extract content
        content = extract_article_content(entry.link)
        
        # Summarize content
        summary = summarize_text(content)
        
        # Prepare message
        message = f"Title: {entry.title}\n\nSummary: {summary}\n\nRead more: {entry.link}"
        
        # Send to Tune Studio
        if send_to_tune_studio(message):
            print(f"Successfully sent summary for: {entry.title}")
        else:
            print(f"Failed to send summary for: {entry.title}")

if __name__ == "__main__":
    main()
