from __future__ import annotations

from typing import Optional
from pydantic import BaseModel, Field
from langchain_core.tools import tool

from ..services.time import get_current_time
from ..services.weather import get_weather
from ..services.banking_faq import search_banking_faq, get_all_faqs
from ..services.exchange_rates import get_exchange_rates, convert_currency


class GetTimeInput(BaseModel):
    timezone: Optional[str] = Field(
        default=None,
        description="დროის სარტყელი, მაგალითად 'UTC', 'Europe/Tbilisi'",
    )


class GetWeatherInput(BaseModel):
    city: str = Field(description="ქალაქის დასახელება, მაგალითად 'Tbilisi'")

class BankingFAQInput(BaseModel):
    query: str = Field(description="ბანკთან დაკავშირებული კითხვა")


class ExchangeRateInput(BaseModel):
    amount: float = Field(description="თანხა კონვერტაციისთვის")
    from_currency: str = Field(description="საწყისი ვალუტა (მაგ: GEL, USD, EUR)")
    to_currency: str = Field(description="სამიზნე ვალუტა (მაგ: GEL, USD, EUR)")


@tool("get_time", args_schema=GetTimeInput)
def tool_get_time(timezone: Optional[str] = None) -> str:
    """ მიმდინარე თარიღი/დრო (ნებისმიერი: კონკრეტულ დროის სარტყელში)."""
    return get_current_time(timezone)


@tool("get_weather", args_schema=GetWeatherInput)
def tool_get_weather(city: str) -> str:
    """ ამინდის მოკლე მიმოხილვა მითითებული ქალაქისთვის (Open‑Meteo)."""
    return get_weather(city)


@tool("search_banking_faq", args_schema=BankingFAQInput)
def tool_search_banking_faq(query: str) -> str:
    """მოძებნე ბანკინგის ხშირად დასმული კითხვები და პასუხები."""
    faq = search_banking_faq(query)
    if faq:
        return f"კითხვა: {faq['question']}\nპასუხი: {faq['answer']}"
    else:
        return "ვერ ვიპოვე პასუხი თქვენს კითხვაზე. გთხოვთ დაუკავშირდეთ TBC ბანკის მხარდაჭერის გუნდს ან გამოიყენეთ ზოგადი ინფო ბანკის შესახებ."


@tool("get_exchange_rates", args_schema=None)
def tool_get_exchange_rates() -> str:
    """მიჩვენე ლარის მიმდინარე სავალუტო კურსები."""
    return get_exchange_rates()


@tool("convert_currency", args_schema=ExchangeRateInput)
def tool_convert_currency(amount: float, from_currency: str, to_currency: str) -> str:
    """გადაიყვანე ვალუტა ერთი ვალუტიდან მეორეში ოფიციალური კურსით."""
    return convert_currency(amount, from_currency, to_currency)

