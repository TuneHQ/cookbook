import json
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from utils import generate_response, generate_pdf_report, generate_evaluation
import base64
import pandas as pd
import os

# Initialize session state
if 'conversation' not in st.session_state:
    st.session_state.conversation = []
if 'user_responses' not in st.session_state:
    st.session_state.user_responses = []
if 'temp_user_responses' not in st.session_state:
    st.session_state.user_responses = []
if 'question_count' not in st.session_state:
    st.session_state.question_count = 0
if 'max_questions' not in st.session_state:
    st.session_state.max_questions = 0
if 'job_description' not in st.session_state:
    st.session_state.job_description = []
if 'questions' not in st.session_state:
    st.session_state.questions = []
if 'interview_started' not in st.session_state:
    st.session_state.interview_started = False
if 'interview_initiated' not in st.session_state:
    st.session_state.interview_initiated = False
if 'api' not in st.session_state:
    st.session_state.api = []
    
# Sidebar for selecting number of questions and difficulty
st.sidebar.title("Smart Interview Simulator")
st.sidebar.subheader("Welcome to Smart Interview Simualtor, an AI bot to simulate interviews, which aids in evaluation and improving answers. Please add your Job Description, Number of Questions, Difficulty, and API Key to start the conversation.")
st.session_state.max_questions = st.sidebar.slider("Number of Questions", 1, 10, 3)
difficulty = st.sidebar.selectbox("Difficulty Level", ["Easy", "Medium", "Hard"])
st.session_state.job_description = st.sidebar.text_area("Job Description", value=st.session_state.job_description, height=200)
st.session_state.api = st.sidebar.text_area('Enter your API Key', value=st.session_state.api, height=20)

# Button to start the conversation
if st.sidebar.button("Start Interview"):
    st.session_state.interview_started = True
    st.session_state.interview_initiated = False  # Reset initiation status
    st.session_state.conversation = []  # Clear conversation history
    st.session_state.user_responses = []
    st.session_state.question_count = 0

# System prompt for the interview
system_prompt = f"""
You are Boss Llama, an advanced AI interviewer. Your goal is to conduct a comprehensive and intelligent interview with the candidate based on the following details:

1. Job Description: {st.session_state.job_description}
2. Difficulty Level: {difficulty}
3. Number of Questions: {st.session_state.max_questions}

Instructions:
1. Start the Interview:
   - Begin by presenting a detailed job description for the role based on the difficulty level and the provided job description. Try to keep this introduction small and to the point as the user already knows what they are interviewing for.
   - Provide a warm welcome message to start the interview and set a positive tone.
2. Generate and Ask Questions:
   - Ask a series of questions, up to the specified number of questions. Ensure these questions are relevant to the job description and appropriately challenging according to the difficulty level.
   - Provide clear and concise prompts that assess the candidate's skills, knowledge, and fit for the role.

3. Conduct the Interview:
   - Engage with the candidate in a conversational manner. If the candidate's responses are vague or insufficient, let them know about it and give them a chance to make it better but count it as one more question.
   - Maintain a professional and supportive tone throughout the interview.
"""

# Check if the interview has started
if st.session_state.interview_started:
    if not st.session_state.interview_initiated:
        
        # Add system prompt to conversation history
        st.session_state.conversation.append({"role": "system", "content": system_prompt})
        
        # Generate bot response for the initial welcome message
        bot_welcome_message = generate_response(st.session_state.conversation, st.session_state.api)
        st.session_state.conversation.append({"role": "bot", "content": bot_welcome_message})
        st.session_state.interview_initiated = True  # Mark interview as initiated

    # Chat Input
    if st.session_state.question_count < st.session_state.max_questions:
        user_input = st.chat_input("You: ")
        if user_input:
            # Append user message to conversation
            st.session_state.conversation.append({"role": "user", "content": user_input})
            st.session_state.user_responses.append(user_input)
            # Generate bot response
            bot_response = generate_response(st.session_state.conversation, st.session_state.api)
            st.session_state.conversation.append({"role": "bot", "content": bot_response})
            st.session_state.question_count += 1
    else:
        st.write("The interview has ended. Click 'Evaluate' to see your performance.")
    
    # Display conversation
    for msg in st.session_state.conversation:
        if msg["role"] != "system":
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

# Button to generate and download PDF report
if st.sidebar.button("Download Evaluation Report"):
    if st.session_state.interview_started:
        evaluations = []
        bot_questions = []
        user_answers = []
        current_question = None

        # Parse conversation to extract questions and answers
        for msg in st.session_state.conversation:
            if msg["role"] == "bot" and "Question" in msg["content"]:
                current_question = msg["content"]
                bot_questions.append(current_question)
            elif msg["role"] == "user" and current_question is not None:
                user_answers.append({
                    "question": current_question,
                    "answer": msg["content"]
                })
                current_question = None  # Reset current question after an answer

        # Generate evaluations for each question-answer pair
        for qa in user_answers:
            question = qa["question"]
            answer = qa["answer"]
            feedback, score = generate_evaluation(question, answer, difficulty, st.session_state.api)
            evaluations.append({
                "Question": f"Q: {question}",
                "Answer": f"A: {answer}",
                "Feedback": feedback,
                "Score": score
            })
        
        # Generate and provide PDF download
        pdf_path = generate_pdf_report(evaluations)
        with open(pdf_path, "rb") as pdf_file:
            st.download_button(
                label="Download PDF Report",
                data=pdf_file.read(),
                file_name="interview_evaluation_report.pdf",
                mime="application/pdf"
            )
        # Clean up temporary file
        os.remove(pdf_path)
    else:
        st.warning("Please start an interview first.")