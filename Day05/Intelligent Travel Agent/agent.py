# agent.py

from tools import get_weather, search_attractions
from transformers import pipeline

def run_travel_agent(destination: str) -> str:
    print(f"[DEBUG] Agent triggered for destination: {destination}")
    # Simulate LLM/API call for weather
    print("[DEBUG] Calling get_weather tool...")
    weather = get_weather(destination)
    print(f"[DEBUG] Weather tool output: {weather}")
    # Simulate LLM/API call for attractions
    print("[DEBUG] Calling search_attractions tool...")
    attractions = search_attractions(destination)
    print(f"[DEBUG] Attractions tool output: {attractions}")
    # Simulate LLM summarization (to be implemented)
    # For now, just combine results
    if not weather and not attractions:
        return "Sorry, I couldn't fetch information for that destination."
    result = f"**🌤 Weather Forecast in {destination}:**\n{weather}\n\n**📍 Top Tourist Attractions in {destination}:**\n{attractions}"
    print(f"[DEBUG] Final output: {result}")
    return result 