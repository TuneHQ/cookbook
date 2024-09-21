import re


class TextCleaner:
    @staticmethod
    def clean_text(text) -> str:
        # Remove Markdown formatting
        text = re.sub(r"\[.*?\]\(.*?\)", "", text)  # Remove links
        text = re.sub(r"[*_~`]", "", text)  # Remove other Markdown symbols
        # Keep only alphanumeric characters and spaces
        text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
        return text.strip()
