from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

def create_chat_openai_instance(tuneai_api_key):
    return ChatOpenAI(
        openai_api_key=tuneai_api_key,
        base_url="https://proxy.tune.app/",
        model="rohan/tune-grok-mixtral-8x7b",
    )

def format_prompt(source_language, target_language, input_text):
    return ChatPromptTemplate.from_messages([
    ("system", "Translate from {source_language} to {target_language}. You respond only in {target_language}"),
    ("user", "{input}")
    ])


def translate(input_text, source_language, target_language, tuneai_api_key):
    llm = create_chat_openai_instance(tuneai_api_key)
    prompt = format_prompt(source_language, target_language, input_text)
    output_parser = StrOutputParser()
    chain = prompt | llm | output_parser
    response = chain.invoke({"input": input_text, "source_language": source_language, "target_language": target_language})
    return response


    