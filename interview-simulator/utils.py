import requests
import json
import streamlit as st
from fpdf import FPDF
from io import BytesIO
import tempfile

# Function to call the API
def generate_response(conversation, apikey):
    url = "https://proxy.tune.app/chat/completions"
    headers = {
        "Authorization": apikey,  # Your API key
        "Content-Type": "application/json"
    }

    # Construct the payload for the API call
    payload = {
        "temperature": 0.9,
        "messages": conversation,
        "model": "meta/llama-3.1-70b-instruct",
        "stream": False,
        "frequency_penalty": 0.2,
        "max_tokens": 500
    }

    # Send the POST request to the API
    response = requests.post(url, headers=headers, data=json.dumps(payload))

    # Check if the request was successful
    if response.status_code == 200:
        # Extract the response from the JSON output
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code} - {response.text}"
    
# Function to generate evaluations on the interview
def generate_evaluation(question, answer, difficulty, apikey):
    url = "https://proxy.tune.app/chat/completions"
    headers = {
        "Authorization": apikey,
        "Content-Type": "application/json"
    }

    payload = {
        "temperature": 0.7,
        "messages": [
            {"role": "system", "content": f"Evaluate the following answer based on the job description difficulty level: {difficulty}."},
            {"role": "user", "content": f"Question: {question}\nAnswer: {answer}"}
        ],
        "model": "meta/llama-3.1-70b-instruct",
        "stream": False,
        "frequency_penalty": 0.2,
        "max_tokens": 500
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        result = response.json()
        feedback = result.get("choices", [{}])[0].get("message", {}).get("content", "No feedback provided")
        score = result.get("choices", [{}])[0].get("score", 0)
        return feedback, score
    except requests.RequestException as e:
        return f"Error: {e}", 0

# Function to generate a PDF report
def generate_pdf_report(evaluations):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    pdf.cell(0, 10, "Interview Evaluation Report", ln=True, align="C")
    pdf.ln(10)  # Add a line break
    
    for evaluation in evaluations:
        pdf.set_font("Arial", style='B', size=12)
        pdf.multi_cell(0, 10, evaluation["Question"])
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, evaluation["Answer"])
        pdf.multi_cell(0, 10, f"Feedback: {evaluation['Feedback']}")
        pdf.multi_cell(0, 10, f"Score: {evaluation['Score']}")
        pdf.ln(5)  # Add a line break

    # Save the PDF to a temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(temp_file.name)
    return temp_file.name