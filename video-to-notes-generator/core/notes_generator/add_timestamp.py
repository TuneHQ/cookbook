import json
import re


class TimestampAdder:
    def __init__(self, notes_location, transcript_location) -> None:
        self.notes_location = notes_location
        self.transcript_location = transcript_location
        self.phrase_to_timestamp = self._load_transcript()

    def _load_transcript(self) -> dict:
        with open(self.transcript_location) as file:
            transcript = json.load(file)
        return {entry["phrase"]: entry["timestamp"] for entry in transcript}

    def _read_notes(self) -> list:
        with open(self.notes_location) as file:
            return file.readlines()

    def _write_notes(self, notes, new_location) -> str:
        with open(new_location, "w") as file:
            file.writelines(notes)
        return new_location

    def add_timestamps(self, new_location) -> str:
        notes = self._read_notes()
        updated_notes = []

        for line in notes:
            updated_line = line
            for phrase, timestamp in self.phrase_to_timestamp.items():
                if re.search(r"\b" + re.escape(phrase) + r"\b", line):
                    updated_line = line.strip() + f" [{timestamp}]\n"
                    break
            updated_notes.append(updated_line)

        return self._write_notes(updated_notes, new_location)


# Example usage:
# adder = TimestampAdder('path/to/notes.md', 'path/to/transcript.json')
# new_file_path = adder.add_timestamps('path/to/new_notes.md')
# print(f"New file saved at: {new_file_path}")
