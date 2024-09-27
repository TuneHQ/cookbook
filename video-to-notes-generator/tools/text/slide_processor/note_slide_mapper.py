import json
import logging

from tools.llm.tune import TuneAI

SYSTEM_INSTRUCTION = """
Task: Contextual Slide Placement
You will receive a fragment of markdown notes and a dictionary of slide titles, indexed by slide numbers. Your objective is to carefully analyze the notes, identify relevant insertion points, and suggest optimal line numbers for slide integration.
Input Format:

    Notes: A markdown text snippet, which may commence from a midpoint in the topic's narrative
    Slides: A dictionary featuring slide numbers as keys and corresponding titles as values, e.g.

JSON

{
  "1": "Slide title 1",
  "2": "Slide title 2",
  ...
}

Output Format:
Return a JSON dictionary with slide numbers as keys and proposed line numbers as values, e.g.
JSON
```json
{
  "1": 5,
  "2": 12,
  ...
}
```
Guidelines:

    Thoroughly examine the markdown notes, taking into account their potential midpoint commencement.
    Determine the most suitable line numbers for slide insertion, ensuring relevance and coherence.
    Exercise discernment; not all slides necessitate insertion. Only recommend placements that harmonize with the content.
    Furnish a dictionary featuring slide numbers as keys and suggested line numbers as values.

Note: Restrict your response to the JSON dictionary, omitting extraneous text or commentary. If a slide's content fails to align with the notes, exclude it from the output dictionary.
"""

logger = logging.getLogger(__name__)


class SlidePlacementProcessor:
    def __init__(self, notes_content, slides, max_length=18000) -> None:
        logger.info("Initializing SlidePlacementProcessor")
        self.notes_content = notes_content
        self.slides = slides
        self.max_length = max_length
        self.ai = TuneAI(system_instruction=SYSTEM_INSTRUCTION)
        logger.info("SlidePlacementProcessor initialized successfully")

    def _split_content(self) -> list:
        chunks = []
        combined_content = self.notes_content + "\n" + json.dumps(self.slides)
        while len(combined_content) > self.max_length:
            split_point = combined_content.rfind(" ", 0, self.max_length)
            if split_point == -1:
                split_point = self.max_length
            chunks.append(combined_content[:split_point])
            combined_content = combined_content[split_point:]
        chunks.append(combined_content)
        return chunks

    def _suggest_slide_placements(self, chunk) -> dict:
        input_data = {
            "notes": chunk,
            "slides": self.slides,
        }
        response = self.ai.generate_content(json.dumps(input_data))
        # print(response)

        # Find the first '{' and the last '}' in the response
        start_index = response.find("{")
        end_index = response.rfind("}")

        # Extract the JSON content
        if start_index != -1 and end_index != -1:
            json_content = response[start_index : end_index + 1]
            return json.loads(json_content)
        return {}

    def process_notes(self) -> dict:
        chunks = self._split_content()
        all_suggestions = {}

        for chunk in chunks:
            suggestions = self._suggest_slide_placements(chunk)
            all_suggestions.update(suggestions)

        return all_suggestions


# Example Usage
if __name__ == "__main__":
    notes_content = """
    # Introduction to Machine Learning
    Machine learning is a field of artificial intelligence that uses statistical techniques to give computer systems the ability to "learn" from data, without being explicitly programmed.

    ## Supervised Learning
    Supervised learning is the machine learning task of learning a function that maps an input to an output based on example input-output pairs.

    ### Linear Regression
    Linear regression is a linear approach to modeling the relationship between a dependent variable and one or more independent variables.

    ### Classification
    Classification is the problem of identifying to which of a set of categories a new observation belongs, on the basis of a training set of data containing observations whose category membership is known.

    ## Unsupervised Learning
    Unsupervised learning is a type of machine learning algorithm used to draw inferences from datasets consisting of input data without labeled responses.

    ### Clustering
    Clustering is the task of dividing the population or data points into a number of groups such that data points in the same groups are more similar to other data points in the same group than those in other groups.

    ### Dimensionality Reduction
    Dimensionality reduction is the process of reducing the number of random variables under consideration by obtaining a set of principal variables.
    """
    slides = {
        1: "Introduction to Machine Learning",
        2: "Supervised Learning",
        3: "Linear Regression",
        4: "Classification",
        5: "Unsupervised Learning",
        6: "Clustering",
        7: "Dimensionality Reduction",
    }
    processor = SlidePlacementProcessor(notes_content, slides)
    slide_placements = processor.process_notes()
    print(slide_placements)
