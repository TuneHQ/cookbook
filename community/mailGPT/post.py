import json
from flask import Flask, request, jsonify,render_template
from flask_cors import CORS
from embedding import retrieve_relevant_emails, load_email_data, prepare_email_embeddings, emails_with_embeddings
from tune_ai import run_tune_ai

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')

def process_query(topic,user_query):
    relevant_emails = retrieve_relevant_emails(topic, emails_with_embeddings)
    relevant_emails_s = []
    for relevant_email in relevant_emails:
        relevant_email_n = {}
        relevant_email_n['subject'] = relevant_email['subject']
        relevant_email_n['from'] = relevant_email['from']
        relevant_email_n['date'] = relevant_email['date']
        relevant_email_n['body'] = relevant_email['body']
        relevant_email_s = str(relevant_email_n)
        relevant_emails_s.append(relevant_email_s)

        print(f"Subject: {relevant_email['subject']}")
        print(f"From: {relevant_email['from']}")
        print(f"Similarity: {relevant_email['similarity']}\n")
    res_from_bot = run_tune_ai(str(relevant_emails_s),user_query)
    return res_from_bot

@app.route('/api/query', methods=['POST'])
def handle_query():
    data = request.get_json()
    topic = data.get('topic', '')
    user_query = data.get('query', '')
    
    if not user_query:
        return jsonify({'error': 'No query asked'}), 400
    
    result = process_query(topic,user_query)
    
    return jsonify({'response': result})

if __name__ == '__main__':
    emails = load_email_data('data/sample.json')
    emails_with_embeddings = prepare_email_embeddings(emails)
    app.run(debug=True, port=5000)