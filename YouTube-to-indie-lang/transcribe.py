from youtube_transcript_api import YouTubeTranscriptApi

# Fetch the transcript
transcript = YouTubeTranscriptApi.get_transcript("8aFqLVQjHTw")

# Initialize variables
total_text = ""
first_start = None
total_duration = 0

# Iterate through the transcript
for entry in transcript:
    if first_start is None:
        first_start = entry['start']
    
    total_duration += entry['duration']
    if total_duration > 120:
        break
    
    total_text += entry['text'] + " "

# Output the results
transcript = total_text.strip()
start_time = first_start

print(transcript, start_time)