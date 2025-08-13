from __future__ import annotations

import httpx
from typing import Dict, Optional

# Using a free exchange rate API (no key required)
_EXCHANGE_URL = "https://api.exchangerate-api.com/v4/latest/GEL"

def get_exchange_rates() -> str:
    """Get current exchange rates for GEL (Georgian Lari)."""
    try:
        with httpx.Client(timeout=10) as client:
            response = client.get(_EXCHANGE_URL)
            if response.status_code != 200:
                return "ვერ ვიპოვე სავალუტო კურსები. გთხოვთ სცადოთ მოგვიანებით."
            
            data = response.json()
            base_currency = data.get("base", "GEL")
            rates = data.get("rates", {})
            
            if not rates:
                return "სავალუტო კურსები ვერ მოიძებნა."
            
            # Format the most common currencies
            common_currencies = ["USD", "EUR", "GBP", "TRY", "RUB"]
            formatted_rates = []
            
            for currency in common_currencies:
                if currency in rates:
                    rate = rates[currency]
                    formatted_rates.append(f"1 GEL = {rate:.4f} {currency}")
            
            if formatted_rates:
                return f"მიმდინარე სავალუტო კურსები:\n" + "\n".join(formatted_rates)
            else:
                return "სავალუტო კურსები ვერ მოიძებნა."
                
    except Exception as e:
        return f"სავალუტო კურსების მიღებისას დაფიქსირდა შეცდომა: {str(e)}"

def convert_currency(amount: float, from_currency: str, to_currency: str) -> str:
    """Convert between currencies using current rates."""
    try:
        with httpx.Client(timeout=10) as client:
            # For cross-currency conversion, we need to get rates from the source currency
            if from_currency == "GEL":
                # Converting from GEL to another currency
                url = f"https://api.exchangerate-api.com/v4/latest/GEL"
                response = client.get(url)
                if response.status_code != 200:
                    return "ვერ ვიპოვე სავალუტო კურსები კონვერტაციისთვის."
                
                data = response.json()
                rates = data.get("rates", {})
                
                if to_currency in rates:
                    converted = amount * rates[to_currency]
                    return f"{amount} GEL = {converted:.2f} {to_currency}"
                else:
                    return f"ვერ ვიპოვე კურსი GEL-დან {to_currency}-ში."
                    
            elif to_currency == "GEL":
                # Converting from another currency to GEL
                url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
                response = client.get(url)
                if response.status_code != 200:
                    return f"ვერ ვიპოვე კურსი {from_currency}-დან GEL-ში."
                
                data = response.json()
                rates = data.get("rates", {})
                
                if "GEL" in rates:
                    converted = amount * rates["GEL"]
                    return f"{amount} {from_currency} = {converted:.2f} GEL"
                else:
                    return f"ვერ ვიპოვე კურსი {from_currency}-დან GEL-ში."
            else:
                # Cross-currency conversion (neither is GEL)
                # First convert from_currency to GEL, then GEL to to_currency
                url1 = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
                response1 = client.get(url1)
                if response1.status_code != 200:
                    return f"ვერ ვიპოვე კურსი {from_currency}-დან GEL-ში."
                
                data1 = response1.json()
                rates1 = data1.get("rates", {})
                
                if "GEL" not in rates1:
                    return f"ვერ ვიპოვე კურსი {from_currency}-დან GEL-ში."
                
                # Convert to GEL first
                gel_amount = amount * rates1["GEL"]
                
                # Now convert GEL to target currency
                url2 = f"https://api.exchangerate-api.com/v4/latest/GEL"
                response2 = client.get(url2)
                if response2.status_code != 200:
                    return f"ვერ ვიპოვე კურსი GEL-დან {to_currency}-ში."
                
                data2 = response2.json()
                rates2 = data2.get("rates", {})
                
                if to_currency in rates2:
                    final_amount = gel_amount * rates2[to_currency]
                    return f"{amount} {from_currency} = {final_amount:.2f} {to_currency}"
                else:
                    return f"ვერ ვიპოვე კურსი GEL-დან {to_currency}-ში."
                
    except Exception as e:
        return f"ვალუტის კონვერტაციისას დაფიქსირდა შეცდომა: {str(e)}"
