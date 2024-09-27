import datetime
import os
import re

from yt_dlp import YoutubeDL


class YouTubeAudioExtractor:
    def __init__(self, url) -> None:
        self.url = url
        self.audio_file = None
        self.download_folder = "downloads"

        # Ensure the download folder exists
        if not os.path.exists(self.download_folder):
            os.makedirs(self.download_folder)

    def get_timestamp(self) -> str:
        """Return the current timestamp in yyyymmddhhmm format."""
        now = datetime.datetime.now(datetime.timezone.utc)
        return now.strftime("%Y%m%d%H%M")

    def sanitize_title(self, title: str) -> str:
        """Sanitize the video title to be used as a filename."""
        return re.sub(r"[^a-zA-Z]", "", title.replace(" ", "_"))

    def download_audio(self) -> tuple:
        """Download audio using yt-dlp and return the file path and video title."""
        try:
            # Define the download options
            ydl_opts = {
                "format": "bestaudio/best",  # Get the best audio quality
                "outtmpl": os.path.join(
                    self.download_folder,
                    "%(title)s.%(ext)s",
                ),  # Save file in the specified folder
                "noplaylist": True,  # Download only the single video
            }
            # Use yt-dlp to download audio
            with YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(self.url, download=False)
                video_title = info_dict.get("title", "Unknown Title")

                # Sanitize the video title
                sanitized_title = self.sanitize_title(video_title)

                # Generate the new filename with sanitized title
                file_extension = info_dict.get("ext", "m4a")
                new_filename = os.path.join(
                    self.download_folder,
                    f"{sanitized_title}.{file_extension}",
                )

                # Check if the file already exists
                if os.path.exists(new_filename):
                    print(f"File already exists: {new_filename}")
                    self.audio_file = new_filename
                    return self.audio_file, sanitized_title

                # Proceed with the download
                info_dict = ydl.extract_info(self.url, download=True)
                original_file = ydl.prepare_filename(info_dict)

                # Rename the downloaded file
                os.rename(original_file, new_filename)

                self.audio_file = new_filename
                print(f"Downloaded audio file: {self.audio_file}")
                return self.audio_file, sanitized_title
        except Exception as e:
            print(f"Error downloading audio: {e}")
            return None, None

    def extract_audio(self) -> tuple:
        """Return the file path and video title."""
        return self.download_audio()


if __name__ == "__main__":
    import sys

    ARGS = 2
    if len(sys.argv) != ARGS:
        print("Usage: python youtube_audio_extractor.py <YouTube URL>")
        sys.exit(1)

    url = sys.argv[1]
    extractor = YouTubeAudioExtractor(url)
    audio_path, video_title = extractor.extract_audio()
    if audio_path:
        print(f"Audio file saved at: {audio_path}")
        print(f"Video title: {video_title}\n")
