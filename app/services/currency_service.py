import httpx

def get_exchange_rates():
    """Get current exchange rates for GEL."""
    try:
        with httpx.Client(timeout=10) as client:
            url = "https://api.exchangerate-api.com/v4/latest/GEL"
            response = client.get(url)
            
            if response.status_code != 200:
                return "Could not fetch exchange rates."
            
            data = response.json()
            rates = data.get("rates", {})
            
            if not rates:
                return "No exchange rates found."
            
            common_currencies = ["USD", "EUR", "GBP", "TRY", "RUB"]
            formatted_rates = []
            
            for currency in common_currencies:
                if currency in rates:
                    rate = rates[currency]
                    formatted_rates.append(f"1 GEL = {rate:.4f} {currency}")
            
            if formatted_rates:
                return "Current exchange rates:\n" + "\n".join(formatted_rates)
            else:
                return "Exchange rates not available."
                
    except Exception as e:
        return f"Exchange rate error: {str(e)}"

def convert_currency(amount, from_currency, to_currency):
    """Convert between currencies."""
    try:
        with httpx.Client(timeout=10) as client:
            if from_currency == "GEL":
                url = f"https://api.exchangerate-api.com/v4/latest/GEL"
                response = client.get(url)
                
                if response.status_code != 200:
                    return f"Could not get rates for GEL to {to_currency}"
                
                data = response.json()
                rates = data.get("rates", {})
                
                if to_currency in rates:
                    converted = amount * rates[to_currency]
                    return f"{amount} GEL = {converted:.2f} {to_currency}"
                else:
                    return f"Rate not found for GEL to {to_currency}"
                    
            elif to_currency == "GEL":
                url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
                response = client.get(url)
                
                if response.status_code != 200:
                    return f"Could not get rates for {from_currency} to GEL"
                
                data = response.json()
                rates = data.get("rates", {})
                
                if "GEL" in rates:
                    converted = amount * rates["GEL"]
                    return f"{amount} {from_currency} = {converted:.2f} GEL"
                else:
                    return f"Rate not found for {from_currency} to GEL"
            else:
                return f"Cross-currency conversion not supported yet."
                
    except Exception as e:
        return f"Currency conversion error: {str(e)}" 