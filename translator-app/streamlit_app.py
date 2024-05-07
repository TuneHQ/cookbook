import streamlit as st
import langchain_translator

st.title('🟣 Tune Translator App')

tuneai_api_key = st.sidebar.text_input('TuneAI API Key', type='password')

with st.form('my_form'):
    user_text = st.text_area("Enter text to translate")
    source_language = st.selectbox("Select source language", ["english", "hindi", "french", "sanskrit", "spanish", "german"])
    target_language = st.selectbox("Select target language", ["english", "hindi", "french", "sanskrit", "spanish", "german"])
    submit_text = st.form_submit_button('Submit')
    if submit_text:
        if not tuneai_api_key.startswith('nbx'):
            st.warning('Please enter your TuneAI API key!', icon='⚠')
        elif source_language == target_language:
            st.warning('Source and target languages must be different!', icon='⚠')
        elif user_text == "":
            st.warning('Please enter text to translate!', icon='⚠')
        elif source_language == "":
            st.warning('Please select a source language!', icon='⚠')
        elif target_language == "":
            st.warning('Please select a target language!', icon='⚠')
        else: 
            # Call the translation function here
            response = langchain_translator.translate(user_text, source_language, target_language, tuneai_api_key)
            st.info(response)
            
        
