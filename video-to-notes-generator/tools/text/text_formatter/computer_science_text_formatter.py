import json
import logging

from tools.llm.tune import TuneAI
from tools.text.text_formatter.text_formatter import TextFormatter

# Define the system instruction constant
SYSTEM_INSTRUCTION = """
For the given transcript, fix the grammar, clean the formatting and do nothing else.
Assume the content is related to computer science, project management, or technology.
"""

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class ComputerScienceTextFormatter(TextFormatter):
    def __init__(self) -> None:
        super().__init__()
        self.ai = TuneAI(system_instruction=SYSTEM_INSTRUCTION)
        logger.info("ComputerScienceTextFormatter initialized with system instruction.")

    def split_text_recursively(self, text, min_size=15000, max_size=25000) -> list:
        if len(text) <= max_size:
            return [text]

        mid = len(text) // 2
        left = text[:mid]
        right = text[mid:]

        if len(left) < min_size:
            return [text]

        return self.split_text_recursively(
            left,
            min_size,
            max_size,
        ) + self.split_text_recursively(right, min_size, max_size)

    def format_text(self, text, domain) -> str:
        logger.info("Starting text formatting process.")
        logger.info(f"Text length: {len(text)} characters.")

        batches = self.split_text_recursively(text)
        logger.info(f"Total batches created: {len(batches)}.")

        processed_batches = []
        for i, batch in enumerate(batches):
            logger.info(
                f"Processing batch {i + 1}/{len(batches)} (length: {len(batch)}).",
            )
            processed_batch = self.ai.generate_content(
                f"Domain: {domain}\nText: {batch}",
            )
            processed_batches.append(processed_batch)
            logger.info(f"Batch {i + 1} processed.")

        # Stitch the processed batches together
        stitched_text = processed_batches[0]
        for i in range(1, len(processed_batches)):
            stitched_text += processed_batches[i]
            logger.info(f"Stitched batch {i + 1} into final text.")

        logger.info("Text formatting process completed.")
        return stitched_text


# Example usage
if __name__ == "__main__":
    # Load text from JSON file
    with open("cache/202408251318.webm.json") as file:
        data = json.load(file)
        text = data["text"]

    domain = "Development"
    formatter = ComputerScienceTextFormatter()
    corrected_text = formatter.format_text(text, domain)
    print(corrected_text)
