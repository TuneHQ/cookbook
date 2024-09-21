import subprocess

def stitch_audio_video(video_file, audio_file, output_file='final_output.mp4'):
    """Stitch the audio file with the video file using ffmpeg."""
    try:
        command = [
            "ffmpeg",
            "-i", video_file,
            "-i", audio_file,
            "-c:v", "copy",
            "-c:a", "aac",
            "-map", "0:v:0",
            "-map", "1:a:0",
            output_file
        ]
        subprocess.run(command, check=True)
        print(f"Final video with audio saved as: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error stitching audio and video: {e}")

if __name__ == "__main__":
    stitch_audio_video("video.mp4", "output.wav")