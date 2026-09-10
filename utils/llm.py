from langchain_google_genai import ChatGoogleGenerativeAI, Modality
from config import settings

def build_llm():
    return ChatGoogleGenerativeAI(
        model=settings.MODEL_NAME,
        api_key=settings.GEMINI_API_KEY,
        temperature=settings.TEMPERATURE
    )

def build_image_llm():
    return ChatGoogleGenerativeAI(
        model=settings.IMAGE_MODEL_NAME,
        api_key=settings.GEMINI_API_KEY,
        response_modalities=[Modality.TEXT, Modality.IMAGE],
    )