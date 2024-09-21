import streamlit as st
from generator import generate_code
from utils import get_supported_languages, get_file_extension

st.title('Code Generator App')

tuneai_api_key = st.sidebar.text_input('TuneAI API Key', type='password')

with st.form('code_generator_form'):
    user_prompt = st.text_area("Enter your code generation prompt")
    programming_language = st.selectbox("Select programming language", get_supported_languages())
    code_style = st.selectbox("Select code style", ["Functional", "Object-Oriented", "Procedural"])
    submit_button = st.form_submit_button('Generate Code')

if submit_button:
    if tuneai_api_key == "":
        st.warning('Please enter your TuneAI API key!', icon='⚠')
    elif user_prompt == "":
        st.warning('Please enter a prompt for code generation!', icon='⚠')
    elif programming_language == "":
        st.warning('Please select a programming language!', icon='⚠')
    elif code_style == "":
        st.warning('Please select a code style!', icon='⚠')
    else:
        with st.spinner('Generating code...'):
            generated_code = generate_code(user_prompt, programming_language, code_style, tuneai_api_key)
            st.code(generated_code, language=programming_language.lower())

        st.download_button(
            label="Download generated code",
            data=generated_code.encode('utf-8'),
            file_name=f"generated_code.{get_file_extension(programming_language)}",
            mime="text/plain"
        )
