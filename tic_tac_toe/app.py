import streamlit as st
from generator import generate_code
st.title('Code Generator App')

tuneai_api_key = st.sidebar.text_input('TuneAI API Key', type='password')

with st.form('code_generator_form'):
    user_prompt = st.text_area("Enter your prompt")
    
   
    submit_button = st.form_submit_button('Lets Play')

if submit_button:
    if tuneai_api_key == "":
        st.warning('Please enter your TuneAI API key!', icon='⚠')
    elif user_prompt == "":
        st.warning('Please enter a prompt for playing Tic Tac Toe', icon='⚠')
    else:
        with st.spinner('Searching for a move...'):
            generated_code = generate_code(user_prompt, tuneai_api_key)
            st.code(generated_code)
