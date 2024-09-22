import json
import os
import requests
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TuneStudioClient:
    def __init__(self, api_key=None, model="meta/llama-3.1-405b-instruct", temperature=0.9, frequency_penalty=0.2, max_tokens=100):
        """
        Initialize the TuneStudioClient with default configurations.
        """
        self.api_key = api_key or os.getenv("TUNE_STUDIO_API_KEY")
        self.model = model
        self.temperature = temperature
        self.frequency_penalty = frequency_penalty
        self.max_tokens = max_tokens
        self.url = "https://proxy.tune.app/chat/completions"
        self.stream = False

    def _get_headers(self):
        """
        Get the headers required for the request.
        """
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def _get_payload(self, messages):
        """
        Construct the payload for the request.
        """
        return {
            "temperature": self.temperature,
            "messages": messages,
            "model": self.model,
            "stream": self.stream,
            "frequency_penalty": self.frequency_penalty,
            "max_tokens": self.max_tokens
        }

    def generate_response(self, messages):
        """
        Send the request and handle the response.
        """
        headers = self._get_headers()
        payload = self._get_payload(messages)
        try:
            response = requests.post(self.url, headers=headers, json=payload)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            return None
        
        if self.stream:
            return self._handle_streaming_response(response)
        else:
            return self._handle_response(response)

    def _handle_response(self, response):
        """
        Handle the non-streaming response.
        """
        try:
            return response.json()
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            return None

    def _handle_streaming_response(self, response):
        """
        Handle the streaming response.
        """
        results = []
        for line in response.iter_lines():
            if line:
                l = line[6:]
                if l != b'[DONE]':
                    try:
                        results.append(json.loads(l))
                    except json.JSONDecodeError as e:
                        logger.error(f"Failed to parse JSON line: {e}")
        return results

    def update_config(self, **kwargs):
        """
        Update the default configurations dynamically.
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

# Usage
if __name__ == "__main__":
    client = TuneStudioClient()
    messages = [
        {"role": "system", "content": "You are TuneStudio"},
        {"role": "user", "content": "Who are you"}
    ]
    response = client.generate_response(messages)
    if response:
        print(response)