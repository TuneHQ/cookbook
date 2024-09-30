import datetime
import os
import re
import subprocess

from yt_dlp import YoutubeDL


class YouTubeVideoDownloader:
    def __init__(self, url) -> None:
        self.url = url
        self.video_file = None
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

    def download_video(self) -> tuple:
        """Download video using yt-dlp and return the file path and video title."""
        try:
            # Define the download options
            ydl_opts = {
                "format": "bestvideo+bestaudio/best",  # Get the best video and audio quality
                "outtmpl": os.path.join(
                    self.download_folder,
                    "%(title)s.%(ext)s",
                ),  # Save file in the specified folder
                "noplaylist": True,  # Download only the single video
            }
            # Use yt-dlp to download video
            with YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(self.url, download=False)
                video_title = info_dict.get("title", "Unknown Title")

                # Sanitize the video title
                sanitized_title = self.sanitize_title(video_title)

                # Generate the new filename with sanitized title
                file_extension = info_dict.get("ext", "mp4")
                new_filename = os.path.join(
                    self.download_folder,
                    f"{sanitized_title}.{file_extension}",
                )

                # Check if the file already exists
                if os.path.exists(new_filename):
                    print(f"File already exists: {new_filename}")
                    self.video_file = new_filename
                    return self.video_file, sanitized_title

                # Proceed with the download
                info_dict = ydl.extract_info(self.url, download=True)
                original_file = ydl.prepare_filename(info_dict)

                # Rename the downloaded file
                os.rename(original_file, new_filename)

                self.video_file = new_filename
                print(f"Downloaded video file: {self.video_file}")
                return self.video_file, sanitized_title
        except Exception as e:
            print(f"Error downloading video: {e}")
            return None, None

    def trim_video(self, input_file: str, output_file: str, duration: int = 120) -> None:
        """Trim the video to the specified duration using ffmpeg."""
        try:
            command = [
                "ffmpeg",
                "-i", input_file,
                "-t", str(duration),
                "-c", "copy",
                output_file
            ]
            subprocess.run(command, check=True)
            print(f"Trimmed video saved as: {output_file}")
        except subprocess.CalledProcessError as e:
            print(f"Error trimming video: {e}")

    def download_and_trim(self) -> tuple:
        """Download and trim the video, then return the file path and video title."""
        video_file, video_title = self.download_video()
        if video_file:
            trimmed_file = os.path.join(self.download_folder, f"{video_title}_trimmed.mp4")
            self.trim_video(video_file, trimmed_file)
            return trimmed_file, video_title
        return None, None


if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=eC6Hd1hFvos"
    downloader = YouTubeVideoDownloader(url)
    video_path, video_title = downloader.download_and_trim()
    if video_path:
        print(f"Trimmed video file saved at: {video_path}")
        print(f"Video title: {video_title}\n")