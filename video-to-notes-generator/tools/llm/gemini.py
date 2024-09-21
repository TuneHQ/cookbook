import logging
import os
import time

import google.generativeai as genai
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GeminiAI:
    def __init__(self, model_name="gemini-1.5-flash", system_instruction=None) -> None:
        load_dotenv()
        genai.configure(api_key=os.getenv("GEMINI_KEY"))
        if system_instruction:
            self.model = genai.GenerativeModel(
                model_name=model_name,
                system_instruction=system_instruction,
            )
        else:
            self.model = genai.GenerativeModel(model_name=model_name)

    def generate_content(self, prompt) -> str:
        max_retries = 3
        wait_time = 60  # seconds

        for attempt in range(1, max_retries + 1):
            try:
                response = self.model.generate_content(prompt)
                return response.text
            except Exception as e:
                logger.warning(f"Attempt {attempt} failed: {e}")
                if attempt < max_retries:
                    logger.info(f"Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                    # get gemini key
                    # select a key at random
                    # reconfigure the gemini api
                    # retry the request
                else:
                    logger.error(f"Failed after {max_retries} attempts: {e}")
                    raise

        return ""  # Add a return statement at the end of the function


# Example usage:
# gemini_ai = GeminiAI()
# response = gemini_ai.generate_content("Write a story about an AI and magic")
# print(response)
