from langchain_google_genai import ChatGoogleGenerativeAI
from config import settings

def build_llm():
    return ChatGoogleGenerativeAI(
        model=settings.MODEL_NAME,
        api_key=settings.GEMINI_API_KEY,
        temperature=settings.TEMPERATURE
    )