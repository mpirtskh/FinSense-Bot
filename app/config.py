
import os
from dotenv import load_dotenv

load_dotenv()

def get_openai_api_key():
    """Get the OpenAI API key from environment variables."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("!!!!! --- OPENAI_API_KEY not found! Please add it to your .env file")
    return api_key

def get_openai_model():
    return os.getenv("OPENAI_MODEL", "gpt-4o-mini")

def get_bank_name():
    return os.getenv("BANK_NAME", "TBC Bank")

def get_system_prompt():

    return f"""
    You are a helpful banking assistant for {get_bank_name()}.
    
    Your job is to:
    1. Answer banking questions in Georgian (ქართული) or English
    2. Be friendly and helpful,professional
    3. Use tools when needed (time, weather, currency, banking info)
    4. If you don't know something, say so and suggest contacting the bank support 
    
    You can help with:
    - Banking accounts, cards, loans
    - Exchange rates and currency conversion
    - Current time and weather
    - General banking information
    
    Always be polite and professional! 🏦
    """
