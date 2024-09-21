import os
from flask import Flask, jsonify, request, render_template
import requests

app = Flask(__name__)

# Configuration for tunestudi chat API
TUNESTUDI_API_URL = 'https://proxy.tune.app/chat/completions'
API_KEY = os.getenv('TUNESTUDI_API_KEY')


if not API_KEY:
    raise ValueError("No API key provided. Please set the TUNESTUDI_API_KEY environment variable.")

@app.route('/api/quote', methods=['GET'])
def get_quote():
    print(API_KEY, "what is PAI key ")
    genre = request.args.get('genre', 'inspirational').lower()
    message = generate_motivational_message(genre)
    return jsonify({'quote': message})

def generate_motivational_message(genre):
    ORG_ID = "Pluralsight"
    headers = {
        'Authorization': f'{API_KEY}',
        'Content-Type': 'application/json',
        # 'X-Org-Id': f'{ORG_ID}'
    }
    prompt = f"Provide a {genre} motivational message."

    payload = {
        "temperature": 0.9,
        "messages": [
            {
                "role": "system",
                "content": "You are TuneStudio"
            },
            {
                "role": "user",
                "content": f"Provide a {genre} motivational message. WIth it's reference Movie name/ Book name"
            }
        ],
        "model": "ramapypi/ramlama",
        "stream": False,
        "penalty": 0.2,
        "max_tokens": 60  # Adjust as per your requirement
    }

    try:
        print(headers, "headers", payload, "payload", TUNESTUDI_API_URL, "key")
        response = requests.post(TUNESTUDI_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        message = data.get('message')
        if message:
            return message.strip()
        else:
            return 'Stay positive and keep pushing forward!'
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return 'Could not retrieve the motivational message due to an HTTP error.'
    except Exception as err:
        print(f"An error occurred: {err}")
        return 'An unexpected error occurred while fetching the motivational message.'

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)