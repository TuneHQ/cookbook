from abc import ABC, abstractmethod


class AudioExtractor(ABC):
    @abstractmethod
    def extract_text(self, audio_file) -> str:
        pass
