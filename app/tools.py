from langchain_core.tools import tool
from app.services.time_service import get_current_time, get_current_date
from app.services.weather_service import get_weather
from app.services.currency_service import get_exchange_rates, convert_currency
from app.services.banking_faq import search_banking_faq, get_all_faqs

@tool
def get_time(timezone=None):
    return get_current_time(timezone)

@tool
def get_date():
    return get_current_date()

@tool
def get_weather_info(city):
    return get_weather(city)

@tool
def get_currency_rates():
    return get_exchange_rates()

@tool
def convert_money(amount, from_currency, to_currency):
    """Convert between currencies."""
    return convert_currency(amount, from_currency, to_currency)

@tool
def search_banking_help(query):
    """Search for banking information."""
    faq = search_banking_faq(query)
    if faq:
        return f"კითხვა: {faq['question']}პასუხი: {faq['answer']}"
    else:
        return "დაუკავშირდით TBC საფორთს"

@tool
def get_banking_overview():
    """Get general banking information."""
    return "ეწვიეთ TBC ბანკის ოფიციალურ საიტს. კიდევ რამით ხომ ვერ დაგეხმარებით?"
