'''from langchain_openai import ChatOpenAI
from config.settings import settings

def get_llm():
    return ChatOpenAI(
        model=settings.MODEL_NAME,
        temperature=0.7,
        openai_api_key=settings.OPENAI_API_KEY
    )'''


'''from openai import OpenAI
import os

def get_llm():
    return OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
    )
'''

from langchain_community.chat_models import ChatOllama

def get_llm():
    return ChatOllama(
        model="llama3",
        temperature=0.7
    )
