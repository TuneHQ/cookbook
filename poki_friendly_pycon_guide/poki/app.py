import time
from dotenv import load_dotenv
from utils import get_response_tunestudio, search_documents

load_dotenv()  # Loads environment variables from .env file

from openai import OpenAI
import streamlit as st
import random
import time

# Set the title of the Streamlit app
st.title("Poki")

# Set the heading for the app
st.header("Welcome to Poki: Your GO-TO PyCon 2024 Help Desk!")
st.subheader("Get instant answers to all your PyCon 2024 questions—from event schedules to speaker details, workshops, ticketing, and more.")

# Display sample questions
st.sidebar.header("Sample Questions")
sample_questions = [
    "What is the schedule for PyCon 2024?",
    "When do ticket sales start?",
    "Who are the keynote speakers this year?",
    "Are there any workshops available?",
    "What is the location of the event?",
    "How can I become a speaker?",
    "What are the COVID-19 guidelines for attendees?",
    "Is there a code of conduct for the conference?",
]
for question in sample_questions:
    st.sidebar.write(f"- {question}")


if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        search = search_documents(prompt)
        stream = get_response_tunestudio(prompt, search.data)
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
