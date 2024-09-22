import streamlit as st
from player import play_game
st.title('Play Tic Tac Toe')

tuneai_api_key = st.sidebar.text_input('TuneAI API Key', type='password')

with st.form('tic_tac_toe_form'):
    user_prompt = st.text_area("Enter your prompt")
    
   
    submit_button = st.form_submit_button('Lets Play')

if submit_button:
    if tuneai_api_key == "":
        st.warning('Please enter your TuneAI API key!', icon='⚠')
    elif user_prompt == "":
        st.warning('Please enter a prompt for playing Tic Tac Toe', icon='⚠')
    else:
        with st.spinner('Searching for a move...'):
            response = play_game(user_prompt, tuneai_api_key)
            st.code(response)
