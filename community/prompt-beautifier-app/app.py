import streamlit as st
from prompt_tools import beautify_prompt

st.title("Tune Prompt Beautifier App")

tuneai_api_key: str = st.sidebar.text_input("TuneAI API Key", type="password")

with st.form("my_form"):
    user_text: str = st.text_area("Enter text")
    bot_function: str = st.selectbox(
        "Select the Bot Function", ["Beautify Prompt", "Generate Prompt"]
    )
    submit_text: bool = st.form_submit_button("Submit")

if submit_text:
    if not tuneai_api_key.strip():
        st.warning("Please enter your TuneAI API Key!", icon="⚠")
    elif not user_text.strip():
        st.warning("Please enter text to generate!", icon="⚠")
    elif not bot_function.strip():
        st.warning("Please select a bot function!", icon="⚠")
    else:
        # Call the beautify_prompt function here
        response: str = beautify_prompt(user_text, bot_function, tuneai_api_key)
        st.info(response)
