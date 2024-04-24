import re

def clean_text(text):
    # Remove extra newlines and spaces
    cleaned_text = re.sub(r'\n+', '\n', text)
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
    # Remove wiki-specific text such as headings, links, categories, and special characters
    cleaned_text = re.sub(r'\[.*?\]', '', cleaned_text)  # Remove text within square brackets
    cleaned_text = re.sub(r'\{.*?\}', '', cleaned_text)  # Remove text within curly braces
    cleaned_text = re.sub(r'\(.*?\)', '', cleaned_text)  # Remove text within parentheses
    cleaned_text = re.sub(r'==.*?==', '', cleaned_text)  # Remove text within double equals
    # Remove special characters
    cleaned_text = re.sub(r'[\|•\t]', '', cleaned_text)
    return cleaned_text.strip()
