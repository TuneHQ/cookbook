from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate


def create_chat_openai_instance(api_key: str) -> ChatOpenAI:
    return ChatOpenAI(
        openai_api_key=api_key,
        base_url="https://proxy.tune.app/",
        model="openai/gpt-4o",
    )


def format_prompt(bot_function: str) -> ChatPromptTemplate:
    if bot_function == "Beautify Prompt":
        system_message = """User will provide a text which is an AI chat prompt.
You need to beautify the prompt for Chat Bot tuning.
Just provide the beautified prompt as the response. Nothing else."""
    elif bot_function == "Generate Prompt":
        system_message = """User will provide a description of what they need.
You need to generate a suitable AI chat prompt based on the description.
Just provide the generated prompt as the response. Nothing else."""
    else:
        system_message = "Invalid bot function selected."

    return ChatPromptTemplate.from_messages(
        [
            ("system", system_message),
            ("user", "{input_text}"),
        ]
    )


def beautify_prompt(input_text: str, bot_function: str, api_key: str) -> str:
    llm = create_chat_openai_instance(api_key)
    prompt_template = format_prompt(bot_function)
    output_parser = StrOutputParser()
    chain = prompt_template | llm | output_parser
    try:
        response = chain.invoke({"input_text": input_text})
    except Exception as e:
        print(f"Error: {e}")
        response = ""
    return response
