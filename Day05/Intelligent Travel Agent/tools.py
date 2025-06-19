# tools.py

import os
from dotenv import load_dotenv
import requests
# from duckduckgo_search import DDGS  # Remove this if switching to Tavily
from tavily import TavilyClient

load_dotenv()

def get_weather(destination: str) -> str:
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        return "Weather API key not found."
    print(f"[DEBUG] Calling WeatherAPI for weather in: {destination}")
    print(f"[DEBUG] API key: {api_key}")
    print(f"[DEBUG] Destination: {destination}")
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={destination}"
    try:
        response = requests.get(url, timeout=10)
        print(f"[DEBUG] WeatherAPI raw response: {response.text}")
        data = response.json()
        if "error" in data:
            return f"Weather API error: {data['error']['message']}"
        location = data["location"]["name"]
        country = data["location"]["country"]
        temp_c = data["current"]["temp_c"]
        condition = data["current"]["condition"]["text"]
        feelslike_c = data["current"]["feelslike_c"]
        humidity = data["current"]["humidity"]
        wind_kph = data["current"]["wind_kph"]
        return (
            f"{location}, {country}: {condition}, {temp_c}°C (feels like {feelslike_c}°C), "
            f"Humidity: {humidity}%, Wind: {wind_kph} kph."
        )
    except Exception as e:
        return f"Error fetching weather: {e}"

def search_attractions(destination: str) -> str:
    print(f"[DEBUG] Searching Tavily for top tourist attractions in: {destination}")
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return "Tavily API key not found."
    client = TavilyClient(api_key=api_key)
    query = f"top tourist attractions in {destination}"
    try:
        results = client.search(query, max_results=5)
        if not results or "results" not in results:
            return "No attractions found."
        attractions = []
        for i, res in enumerate(results["results"], 1):
            title = res.get('title', 'No title')
            snippet = res.get('content', '')
            attractions.append(f"{i}. **{title}** - {snippet}")
        return "\n".join(attractions)
    except Exception as e:
        return f"Error searching for attractions: {e}" 