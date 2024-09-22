from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI

def hotel_concierg(llm_key, support_type, user_input):
    chat_model = ChatOpenAI(
    openai_api_key=llm_key,
    openai_api_base="https://proxy.tune.app/",
    model_name="aniket7/hotel-concierge"
    )

    out = chat_model.predict(user_input)
    return out
