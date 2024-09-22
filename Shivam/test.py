import streamlit as st
from joker import joker_code
st.title('I am a Comedian')

tuneai_api_key = st.sidebar.text_input('TuneAI API Key', type='password')

with st.form('joke_form'):
    user_prompt = st.text_area("Enter your input")


    submit_button = st.form_submit_button('Submit')

if submit_button:
    if tuneai_api_key == "":
        st.warning('Enter your TuneAI API key!', icon='⚠')
    elif user_prompt == "":
        st.warning('Please enter a prompt!', icon='⚠')
    else:
        with st.spinner('Generating code...'):
            joke = joker_code(user_prompt, tuneai_api_key)
            st.code(joke)
