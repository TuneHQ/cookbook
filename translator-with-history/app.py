import streamlit as st
from translator import translate, save_translation_history, get_translation_history

st.title('Tune Translator Chat App')

tuneai_api_key = st.sidebar.text_input('TuneAI API Key', type='password')
tuneai_model = st.sidebar.text_input('TuneAI Model')

with st.form('my_form'):
    user_text = st.text_area("Enter text to translate")
    source_language = st.selectbox("Select source language", ["English", "Hindi", "French", "Sanskrit", "Spanish", "German"])
    target_language = st.selectbox("Select target language", ["English", "Hindi", "French", "Sanskrit", "Spanish", "German"])
    submit_text = st.form_submit_button('Submit')
    response = None

    if submit_text:
        if not tuneai_api_key:
            st.warning('Please enter your TuneAI API key!', icon='⚠')
        elif not tuneai_model:
            st.warning('Please enter your TuneAI model!', icon='⚠')
        elif source_language == target_language:
            st.warning('Source and target languages must be different!', icon='⚠')
        elif user_text == "":
            st.warning('Please enter text to translate!', icon='⚠')
        elif source_language == "":
            st.warning('Please select a source language!', icon='⚠')
        elif target_language == "":
            st.warning('Please select a target language!', icon='⚠')
        else:
            response = translate(user_text, source_language, target_language, tuneai_api_key, tuneai_model)
            st.info(response)

        # Save translation history
        save_translation_history(source_language, target_language, user_text, response)
        # Display translation history
        translation_history = get_translation_history()
        st.write("Translation History:")
        for row in translation_history:
            st.write(f"{row[3]} -> {row[4]}")