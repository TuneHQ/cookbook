import json
import os
import time
import requests
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TuneAI:
    def __init__(self, model_name="meta/llama-3.1-405b-instruct", temperature=0.9, frequency_penalty=0.2, stream=False) -> None:
        load_dotenv()
        self.api_key = os.getenv("TUNE_KEY")
        self.url = "https://proxy.tune.app/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        self.model = model_name
        self.temperature = temperature
        self.frequency_penalty = frequency_penalty
        self.stream = stream

    def generate_content(self, prompt, language) -> str:
        max_retries = 3
        wait_time = 60  # seconds

        data = {
            "temperature": self.temperature,
            "messages": [
                {
                    "role": "system",
                    "content": f"You are transcriber and your only task is to convert the given text from english to the given language. You should respond only and only with the converted text. Do not return anything before and after the converted text. Your response should consist of text only and only in the given language."
                },
                {
                    "role": "user",
                    "content": f"Conversion language: {language}. Input text: {prompt}"
                }
            ],
            "model": self.model,
            "stream": self.stream,
            "frequency_penalty": self.frequency_penalty
        }

        for attempt in range(1, max_retries + 1):
            try:
                response = requests.post(self.url, headers=self.headers, json=data)
                if self.stream:
                    for line in response.iter_lines():
                        if line:
                            l = line[6:]
                            if l != b'[DONE]':
                                return json.loads(l)
                else:
                    return response.json()
            except Exception as e:
                logger.warning(f"Attempt {attempt} failed: {e}")
                if attempt < max_retries:
                    logger.info(f"Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    logger.error(f"Failed after {max_retries} attempts: {e}")
                    raise

        return ""  # Add a return statement at the end of the function

# Example usage:
# tune_ai = TuneAI()
# response = tune_ai.generate_content("what is the radius of sun")
# print(response)