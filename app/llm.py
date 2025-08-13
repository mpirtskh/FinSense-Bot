from langchain_openai import ChatOpenAI
from app.config import get_openai_api_key, get_openai_model

def create_llm():
    """Create and configure the OpenAI language model."""
    api_key = get_openai_api_key()
    model = get_openai_model()
    
    return ChatOpenAI(
        model=model,
        api_key=api_key,
        temperature=0.1
    )

