from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

def create_chat_openai_instance(tuneai_api_key):
    return ChatOpenAI(
        openai_api_key=tuneai_api_key,
        base_url="https://proxy.tune.app/",
        model="openai/gpt-4o",
    )

def format_prompt( user_prompt):
    return ChatPromptTemplate.from_messages([
    ("system", "You are an expert in tic tac toe. Play a game of tic tac toe."),
    ("user", "{input}")
    ])

def generate_code(user_prompt, tuneai_api_key):
    llm = create_chat_openai_instance(tuneai_api_key)
    prompt = format_prompt(user_prompt)
    output_parser = StrOutputParser()
    chain = prompt | llm | output_parser
    response = chain.invoke({"input": user_prompt})
    
    return response