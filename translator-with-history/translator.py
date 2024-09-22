from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import sqlite3

conn = sqlite3.connect("translation_history.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS translation_history (
        id INTEGER PRIMARY KEY,
        source_language TEXT,
        target_language TEXT,
        input_text TEXT,
        translated_text TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
""")

def save_translation_history(source_language, target_language, input_text, translated_text):
    cursor.execute("""
        INSERT INTO translation_history (source_language, target_language, input_text, translated_text)
        VALUES (?, ?, ?, ?);
    """, (source_language, target_language, input_text, translated_text))
    conn.commit()

def get_translation_history():
    cursor.execute("""
        SELECT * FROM translation_history;
    """)
    return cursor.fetchall()

# Language mapping dictionary
language_map = {
    "English": "en",
    "Hindi": "hi",
    "French": "fr",
    "Sanskrit": "sa",
    "Spanish": "es",
    "German": "de"
}

def create_chat_openai_instance(tuneai_api_key, tuneai_model):
    return ChatOpenAI(
        openai_api_key=tuneai_api_key,
        base_url="https://proxy.tune.app/",
        model=tuneai_model,
    )

def format_prompt(source_language, target_language, input_text):
    source_lang_code = language_map[source_language]
    target_lang_code = language_map[target_language]
    return ChatPromptTemplate.from_messages([
        ("system", f"Translate from {source_lang_code} to {target_lang_code}. You respond only in {target_lang_code}"),
        ("user", input_text)
    ])

def translate(input_text, source_language, target_language, tuneai_api_key, tuneai_model):
    try:
        llm = create_chat_openai_instance(tuneai_api_key, tuneai_model)
        prompt = format_prompt(source_language, target_language, input_text)
        output_parser = StrOutputParser()
        chain = prompt | llm | output_parser
        response = chain.invoke({"input": input_text, "source_language": source_language, "target_language": target_language})
        translated_text = response.strip()
        return translated_text
    except Exception as e:
        return f"Error: {str(e)}"
