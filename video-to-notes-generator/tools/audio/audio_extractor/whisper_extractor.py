import json
import logging
import os

import whisper

from tools.audio.audio_extractor.extractor import AudioExtractor

logger = logging.getLogger(__name__)


class WhisperAudioExtractor(AudioExtractor):
    def __init__(self, model_size="base") -> None:
        logger.info(f"Initializing Whisper model with size: {model_size}")
        self.model = whisper.load_model(model_size, device="cuda")
        logger.info("Whisper model initialized successfully")

    def extract_text(self, audio_file, language) -> tuple:
        # Ensure cache directory exists
        cache_dir = "cache"
        os.makedirs(cache_dir, exist_ok=True)

        # Generate cache file path
        cache_file = os.path.join(cache_dir, f"{os.path.basename(audio_file)}.json")

        # Check if transcription result is already cached
        if os.path.exists(cache_file):
            logger.info(
                f"Reading transcription from cache for audio file: {audio_file}",
            )
            with open(cache_file) as f:
                cached_result = json.load(f)
            return cached_result["text"], cached_result["segments"]

        logger.info(f"Starting transcription for audio file: {audio_file}")
        # Transcribe the audio
        result = self.model.transcribe(audio_file, language=language)
        logger.info(f"Transcription completed for audio file: {audio_file}")
        logger.debug(f"Transcription result: {result['text']}")

        # result = {
        #     "text": result["text"],
        # }
        # Save the result to cache
        with open(cache_file, "w") as f:
            json.dump(result, f)

        # Return the recognized text
        return result["text"], result["segments"]


# sample usage
if __name__ == "__main__":
    whisper_audio_extractor = WhisperAudioExtractor()
    text = whisper_audio_extractor.extract_text(
        "downloads/202408251318.webm",
    )
    print(text)
