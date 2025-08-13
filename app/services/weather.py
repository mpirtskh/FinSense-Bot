from __future__ import annotations

import httpx
from typing import Any, Dict, Optional

_GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
_FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


def get_weather(city: str) -> str:
    """Return a short textual weather summary for a given city using Open-Meteo.

    This uses free endpoints and does not require an API key.
    """
    if not city or not city.strip():
        return "გთხოვთ მიუთითოთ ქალაქი"

    city = city.strip()

    with httpx.Client(timeout=10) as client:
        # 1) Geocode the city to lat/lon
        geo_params = {"name": city, "count": 1, "language": "en", "format": "json"}
        geo_resp = client.get(_GEOCODE_URL, params=geo_params)
        if geo_resp.status_code != 200:
            return f"Could not fetch geocoding for {city}."
        geo_data = geo_resp.json()
        results = geo_data.get("results") or []
        if not results:
            return f"ვერ ვიპოვე ქალაქი: '{city}'."

        top = results[0]
        latitude = top["latitude"]
        longitude = top["longitude"]
        resolved_name = top.get("name", city)
        country = top.get("country", "")

        # 2) Get current weather
        forecast_params = {
            "latitude": latitude,
            "longitude": longitude,
            "current_weather": True,
        }
        fc_resp = client.get(_FORECAST_URL, params=forecast_params)
        if fc_resp.status_code != 200:
            return f"ვერ ვიპოვე ამინდის მონაცემები ქალაქისთვის: {resolved_name}."
        fc_data = fc_resp.json()
        current = fc_data.get("current_weather") or {}
        if not current:
            return f"ვერ ვიპოვე ამინდის მონაცემები მითითებული ქალაქისთვის: {resolved_name}."

        temperature_c = current.get("temperature")
        windspeed_kmh = current.get("windspeed")
        weather_code = current.get("weathercode")

        parts = []
        if temperature_c is not None:
            parts.append(f"{round(temperature_c, 1)}°C")
        if windspeed_kmh is not None:
            parts.append(f"wind {round(windspeed_kmh)} km/h")
        if weather_code is not None:
            parts.append(f"code {weather_code}")

        details = ", ".join(parts) if parts else "unavailable"
        location_label = f"{resolved_name}, {country}".strip().strip(',')
        return f"ამინდი {location_label}: {details}."
