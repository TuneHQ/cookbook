import markdown
from bs4 import BeautifulSoup

from tools.text.matching.fuzzy import FuzzyMatcher
from tools.text.text_formatter.text_cleaner import TextCleaner


class TimestampedNoteProcessor:
    def __init__(self, segments) -> None:
        self.segments = segments

    def process_notes(self, notes, youtube_url) -> tuple:
        matches = 0
        new_notes = []
        for line in notes.splitlines():
            stripped_line = line.strip()

            # Convert Markdown to HTML for each line
            html_content = markdown.markdown(stripped_line)

            # Use BeautifulSoup to extract plain text from HTML
            soup = BeautifulSoup(html_content, "html.parser")
            plain_text = soup.get_text()

            cleaned_line = TextCleaner.clean_text(plain_text)
            link = FuzzyMatcher.fuzzy_matching(self.segments, cleaned_line, youtube_url)
            if link:
                new_line = f"{line} [🔉]({link})"
                matches += 1
            else:
                new_line = line
            new_notes.append(new_line)

        new_notes_content = "\n".join(new_notes)
        return new_notes_content, matches
