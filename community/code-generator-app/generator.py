from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from utils import extract_between_backticks

def create_chat_openai_instance(tuneai_api_key):
    return ChatOpenAI(
        openai_api_key=tuneai_api_key,
        base_url="https://proxy.tune.app/",
        model="openai/gpt-4o",
    )

def format_prompt(programming_language, code_style, user_prompt):
    return ChatPromptTemplate.from_messages([
    ("system", "You are an expert code generator. Generate code in {programming_language} using {code_style} style."),
    ("user", "{input}")
    ])

def generate_code(user_prompt, programming_language, code_style, tuneai_api_key):
    llm = create_chat_openai_instance(tuneai_api_key)
    prompt = format_prompt(programming_language, code_style, user_prompt)
    output_parser = StrOutputParser()
    chain = prompt | llm | output_parser
    response = chain.invoke({"input": user_prompt, "programming_language": programming_language, "code_style": code_style})
    code_snippet = extract_between_backticks(response.strip())
    return code_snippet.strip()