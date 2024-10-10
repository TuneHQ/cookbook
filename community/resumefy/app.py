import streamlit as st
import requests
import PyPDF2
import json

# Set TuneStudio API credentials and URL
TUNE_API_URL = "https://proxy.tune.app/chat/completions"
TUNE_API_KEY = "YOUR_API_KEY"  # Replace with your actual TuneStudio API key
MODEL = "anthropic/claude-3.5-sonnet"  # The model you want to use

headers = {
    "Authorization": f"Bearer {TUNE_API_KEY}",
    "Content-Type": "application/json",
}


def parse_pdf(file):
    """Parses uploaded PDF file and returns text."""
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        text += page.extract_text()
    return text


def get_tune_response(messages, temperature=0.8, max_tokens=900, stream=False):
    """Sends a prompt and messages to the TuneStudio API and gets the response."""
    data = {
        "temperature": temperature,
        "messages": messages,
        "model": MODEL,
        "stream": stream,
        "frequency_penalty": 0,
        "max_tokens": max_tokens,
    }
    response = requests.post(TUNE_API_URL, headers=headers, json=data)

    if stream:
        # Handle streaming responses (if TuneStudio supports it)
        for line in response.iter_lines():
            if line:
                l = line[6:]
                if l != b"[DONE]":
                    return json.loads(l)
    else:
        return response.json()


def main():
    st.title("Resumefy: all judgy and grumpy!")

    # Step 1: Upload the resume PDF
    uploaded_file = st.file_uploader("Upload your resume as a PDF", type="pdf")

    if uploaded_file:
        # Step 2: Parse the PDF and extract text
        with st.spinner("Reading through your resume..."):
            resume_text = parse_pdf(uploaded_file)
            st.success("PDF processed successfully!")

        # Display extracted text for transparency
        st.subheader("Mirror of your life:")
        st.text_area("Resume Text", value=resume_text, height=300)

        # Step 3: Generate a prompt to send to the LLM
        initial_prompt = (
            f"I have the following resume. Can you please review it and provide feedback? "
            f"Here is the resume:\n{resume_text}\n"
            "Please include suggestions for improvement and general recommendations."
        )

        # Prepare messages for the chat completion API
        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant that reviews resumes.",
            },
            {"role": "user", "content": initial_prompt},
        ]

        # Step 4: Send the prompt to TuneStudio and get the feedback
        if st.button("Judge Me!"):
            with st.spinner("Sending resume to Resumefy for feedback..."):
                feedback = get_tune_response(messages)
            st.subheader("Feedback:")
            st.write(feedback["choices"][0]["message"]["content"])

            # Add feedback to the conversation history
            messages.append(
                {
                    "role": "assistant",
                    "content": feedback["choices"][0]["message"]["content"],
                }
            )

            # Prefilled prompts for follow-up questions
            st.subheader("Ask Further Questions:")
            st.write("Here are some suggestions you might ask the model:")
            suggested_prompts = [
                "Can you suggest ways to highlight my skills better?",
                "What are the most important points I should focus on?",
                "How can I make my resume stand out?",
                "Can you help me tailor this resume for a specific job role?",
            ]

            # Display the prefilled prompts as buttons
            for prompt in suggested_prompts:
                if st.button(prompt):
                    with st.spinner(f"Asking: '{prompt}'..."):
                        # Send the follow-up question to TuneStudio
                        messages.append({"role": "user", "content": prompt})
                        follow_up_response = get_tune_response(messages)
                        st.subheader(f"Response to: '{prompt}'")
                        st.write(follow_up_response["choices"][0]["message"]["content"])
                        messages.append(
                            {
                                "role": "assistant",
                                "content": follow_up_response["choices"][0]["message"][
                                    "content"
                                ],
                            }
                        )

            # Step 5: Allow the user to ask custom follow-up questions
            st.subheader("Ask a Custom Question:")
            user_question = st.text_input("Your question:")

            if st.button("Submit Question"):
                if user_question.strip() != "":
                    with st.spinner(f"Asking: '{user_question}'..."):
                        # Send the custom question to TuneStudio
                        messages.append({"role": "user", "content": user_question})
                        custom_response = get_tune_response(messages)
                        st.subheader(f"Response to: '{user_question}'")
                        st.write(custom_response["choices"][0]["message"]["content"])
                        messages.append(
                            {
                                "role": "assistant",
                                "content": custom_response["choices"][0]["message"][
                                    "content"
                                ],
                            }
                        )


if __name__ == "__main__":
    main()
