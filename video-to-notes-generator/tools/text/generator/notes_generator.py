import logging

from tools.llm.tune import TuneAI

# Always Color the notes using inline html to make them appear nice and readable.
# eg: <span style="color:blue">some blue text</span>.
# Markdown formatting wont work inside the <span> tag.
# Apply the markdown formatting outside the <span> tag.

SYSTEM_INSTRUCTION = """
Task: Convert Transcript to Markdown Notes

Inputs: Title, transcript.

Output: Comprehensive, well-structured notes in Markdown.

Instructions:

Convert the transcript into detailed, organized notes.
Capture all key points, examples, and explanations without missing critical details.
Follow the sequence of the transcript, ensuring clarity and coherence.
Highlight important concepts, quotes, and terms.
You may include paragraphs, explainers, eli5, and summaries for better understanding.
The notes should be detailed enough that anyone reading them would have a clear understanding of everything discussed in the talk/lecture.
The notes should not miss any critical points or examples mentioned in the transcript.
Ensure the notes are easy to read, organized, and highlight important concepts, quotes, and terms.
Include important key points, examples, and explanations.

### **Instructions:**

1. **Formatting:**
   - Use **Markdown** for all formatting.
   - Create **sections** and **subsections** based on the content.
   - Use **bullet points** for key points, ensuring ease of reading.
   - Use paragraphs to elaborate on key points and provide additional context.
   - Use tables where necessary.
   - Use proper formating for comparisons.
   - Highlight important terms using:
     - **Bold** for critical terms or concepts.
     - *Italics* for emphasis.
     - `Code formatting` for technical terms or code snippets.
     - > Blockquotes for notable quotes or one-liners.
     
2. **Content Structure:**
   - **Follow the sequence** of the original transcript.
   - **Divide content into sections and subsections** as logically as possible:
     - **Introduction**: Briefly summarize the opening remarks or agenda.
     - **Main Sections**: Break down the key topics discussed in the talk. Each section should have a summary at the beginning.
     - **Subsections**: Further divide sections if needed. Include summaries for clarity.
     - **Conclusion**: Summarize the closing remarks and any final thoughts.
   - Include **summaries** at the beginning of each section and subsection to encapsulate the core ideas.
   - Create special sections as needed:
     - **Points to Ponder**: Reflective or thought-provoking points.
     - **Facts/Trivia/Tidbits**: Interesting facts or side information.
     - **Key Takeaways**: Summarize the essential points at the end.
   - Insert **important quotes, good one-liners, or noteworthy statements** wherever they naturally fit into the notes.
   - Always try to add some sentences and quotes from the speaker to maintain the authenticity of the notes.

3. **Content Integration:**
   - Ensure that **all sections are logically connected**, and the flow of information remains coherent and easy to follow.
   - Do not include continued, incomplete sentences from the transcript. **Complete the sentences** to maintain readability.
   - At the end, the notes will be compiled as one document, so ensure that the **formatting is consistent** throughout.
   - You do not need to include "continued" in any place.

4. **Additional Considerations:**
   - Do not ask any follow-up questions or clarifications. Start directly with the note creation.
   - Assume that the content is related to consulting, economy, maths, physics, computer science, project management, or technology unless specified otherwise.
   - Maintain a professional tone, keeping the audience in mind (likely students, professionals, or researchers).
   - The notes should be **concise but informative**, capturing the essence of the talk without unnecessary detail.
   - Put longer paragraphs where it would help in explaining or elaborating a concept.

### **Expected Output:**

A Markdown-formatted document with well-structured notes that:
- Have good colouring for readability.
- Reflects the sequence of the original transcript.
- Includes sections, subsections, summaries, paragraph, explanations and bullet points.
- Highlights important terms, quotes, and one-liners.
- Provides clear, easy-to-read notes that are informative and organized.
"""

DOMAIN = (
    "Computer Science, Project Management, Technology, Mathematics, Sciences, Research"
)

logger = logging.getLogger(__name__)


class NotesGenerator:
    def __init__(self, title, transcript) -> None:
        logger.info(f"Initializing NotesGenerator with title: {title}")
        self.title = title
        self.transcript = transcript
        self.ai = TuneAI(system_instruction=SYSTEM_INSTRUCTION)
        logger.info("NotesGenerator initialized successfully")

    def split_transcript(self, transcript, max_length=18000) -> list:
        chunks = []
        while len(transcript) > max_length:
            split_point = transcript.rfind(" ", 0, max_length)
            if split_point == -1:
                split_point = max_length
            chunks.append(transcript[:split_point])
            transcript = transcript[split_point:]
        chunks.append(transcript)
        return chunks

    def generate_notes_for_chunk(self, chunk, chunk_number, previous_summary) -> str:
        chunk_with_context = (
            f"Chunk {chunk_number}\nPrevious Summary: {previous_summary}\n\n{chunk}"
        )
        return self.ai.generate_content(chunk_with_context)

    def generate_notes(self) -> str:
        chunks = self.split_transcript(self.transcript)
        all_notes = []
        previous_summary = ""

        for i, chunk in enumerate(chunks):
            chunk_number = i + 1
            notes = self.generate_notes_for_chunk(chunk, chunk_number, previous_summary)
            all_notes.append(notes)
            previous_summary = self.extract_summary_from_notes(notes)

        return "\n\n".join(all_notes)

    def extract_summary_from_notes(self, notes) -> str:
        # for now, let's just return the first 2 and last two lines as summary
        lines = notes.split("\n")
        return "\n".join(lines[:2] + lines[-2:])


# Example Usage
if __name__ == "__main__":
    title = "Title of the Talk"
    transcript = """
    This is the transcript of the talk. It contains the spoken words of the presenter or presenters in the session. The transcript may include speech errors and filler words.
    """
    notes_generator = NotesGenerator(title, transcript)
    notes = notes_generator.generate_notes()
    print(notes)
