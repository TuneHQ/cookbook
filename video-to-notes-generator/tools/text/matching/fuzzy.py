import nltk
from fuzzywuzzy import fuzz
from nltk.tokenize import word_tokenize

# Constants
MIN_TOKEN_LENGTH = 4
MATCH_THRESHOLD = 50


nltk.download("punkt")


class FuzzyMatcher:
    @staticmethod
    def fuzzy_matching(segments, line, youtube_url) -> str:
        best_match = 0
        best_link = None
        line_tokens = word_tokenize(line.lower())
        line_tokens = [token for token in line_tokens if token.isalpha()]
        if len(line_tokens) < MIN_TOKEN_LENGTH:
            return 0
        for segment in segments:
            text = segment["text"]
            tokens = word_tokenize(text.lower())
            tokens = [token for token in tokens if token.isalpha()]
            if len(tokens) < MIN_TOKEN_LENGTH:
                continue
            ratio = fuzz.ratio(text.lower(), line.lower())
            if ratio > best_match:
                best_match = ratio
                start_time = int(segment["start"])
                best_link = f"{youtube_url}?t={start_time}"
        return (
            best_link if best_match > MATCH_THRESHOLD else 0
        )  # Adjust the threshold as needed
