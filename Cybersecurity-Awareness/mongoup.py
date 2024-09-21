import json
import requests
import requests
from pymongo import MongoClient
from pymongo.server_api import ServerApi

import time

# MongoDB connection URI
uri = "mongodb+srv://itsrohanvj:U2IZLM2Q6zY5mkck@innothon.su9fje6.mongodb.net/?retryWrites=true&w=majority&appName=Innothon" 
client = MongoClient(uri, server_api=ServerApi('1'), tls=True)
db = client['innothon_db']
quiz_collection = db['cyber_quiz']
def fetch_questions():
    stream = False
    url = "https://proxy.tune.app/chat/completions"
    headers = {
        "Authorization": "sk-tune-ZaO0F5cw5a5iqKYmDUTIsowJapvViURZJNA",
        "Content-Type": "application/json",
    }
    data = {
    "temperature": 0.65,
        "messages":  [
    {
        "role": "system",
        "content": [
        {
            "type": "text",
            "text": "You are a helpful assistant. Provide cybersecurity best practices questions and answers. Format the response as follows: for each question, provide a line starting with the question text like this: - Question:, followed by an answer line starting with \"- Answer: - True\" or \"- Answer: - False\". Separate each question-answer pair with an empty line."
        }
        ]
    },
    {
        "role": "user",
        "content": [
        {
            "type": "text",
            "text": "Give me 5 questions and answers based on cybersecurity best practices where answers are True or False. Use the specified format for easy parsing."
        }
        ]
    }
    ],
        "model": "openai/gpt-4o",
        "stream": stream,
        "frequency_penalty":  0,
        "max_tokens": 900
    }
    response = requests.post(url, headers=headers, json=data)
    if stream:
        for line in response.iter_lines():
            if line:
                l = line[6:]
                if l != b'[DONE]':
                    print(json.loads(l))
    else:
        data=response.json()
        content = data['choices'][0]['message']['content']
        print(content)
        return content

    # Function to parse the OpenAI response
def parse_questions(content):
    if not content:
        print("No content to parse.")  # Debugging print
        return []

    lines = content.strip().split('\n')
    questions = []

    print("Raw lines:", lines)  # Debugging print to see the raw lines

    i = 0
    while i < len(lines):
        # Skip any empty lines
        if lines[i].strip() == '':
            i += 1
            continue

        # Check if the line starts with '- Question: '
        if i + 1 < len(lines) and lines[i].startswith('- Question:') and lines[i + 1].startswith('- Answer:'):
            question_line = lines[i].strip()
            answer_line = lines[i + 1].strip()

            # Extract and clean up question and answer
            answer = answer_line.replace('- Answer: - ', '').strip().lower()
            question = question_line.replace('- Question: ', '').strip()
            
            print(f"Question line: '{question_line}'")  # Debugging print
            print(f"Answer line: '{answer_line}'")  # Debugging print

            if answer in ['true', 'false']:
                questions.append((answer.capitalize(), question))
                print(f"Added question: '{question}' with answer: '{answer.capitalize()}'")  # Debugging print
        
        # Move to the next question-answer pair
        i += 3  # Move past question, answer, and empty line

    print("Parsed questions:", questions)  # Debugging print to see the final parsed questions
    return questions

# Function to update MongoDB collection
def update_collection(questions):
    if not questions:
        print("No questions to update in the database.")  # Debugging print
        return

    # Prepare new data with the question as the key
    new_data = {question: answer for answer, question in questions}

    try:
        # Delete all existing records
        quiz_collection.delete_many({})
        
        # Insert a new document with the new data
        quiz_collection.insert_one(new_data)
        print(f"Inserted new document with {len(new_data)} questions and answers.")
    except Exception as e:
        print(f"Error updating MongoDB collection: {e}")

# Main function
def main():
    while True:
        content = fetch_questions()
        if content:
            questions = parse_questions(content)
            if questions:
                update_collection(questions)
        # Wait for 90 seconds before fetching again
        time.sleep(180)

if __name__ == '__main__':
    main()