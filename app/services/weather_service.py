import httpx

def get_weather(city):
    """Get weather for a city using free Open-Meteo API."""
    if not city or not city.strip():
        return "Please provide a city name."
    
    city = city.strip()
    
    try:
        with httpx.Client(timeout=10) as client:
            geo_url = "https://geocoding-api.open-meteo.com/v1/search"
            geo_params = {"name": city, "count": 1, "language": "en", "format": "json"}
            geo_resp = client.get(geo_url, params=geo_params)
            
            if geo_resp.status_code != 200:
                return f"Could not find location: {city}"
            
            geo_data = geo_resp.json()
            results = geo_data.get("results", [])
            
            if not results:
                return f"Location not found: {city}"
            
            location = results[0]
            lat = location["latitude"]
            lon = location["longitude"]
            city_name = location.get("name", city)
            country = location.get("country", "")
            
            weather_url = "https://api.open-meteo.com/v1/forecast"
            weather_params = {
                "latitude": lat,
                "longitude": lon,
                "current_weather": True
            }
            
            weather_resp = client.get(weather_url, params=weather_params)
            if weather_resp.status_code != 200:
                return f"Could not get weather for {city_name}"
            
            weather_data = weather_resp.json()
            current = weather_data.get("current_weather", {})
            
            if not current:
                return f"No weather data for {city_name}"
            
            temp = current.get("temperature")
            wind = current.get("windspeed")
            
            location_label = f"{city_name}, {country}".strip().strip(',')
            weather_info = f"Weather in {location_label}: {temp}°C"
            
            if wind:
                weather_info += f", wind {wind} km/h"
            
            return weather_info
            
    except Exception as e:
        return f"Weather service error: {str(e)}" 