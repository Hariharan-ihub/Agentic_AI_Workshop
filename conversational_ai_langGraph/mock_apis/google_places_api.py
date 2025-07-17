import os
import requests

def search_places(location, category):
    """
    Uses Google Places API to search for businesses by location and category.
    """
    api_key = os.getenv("GOOGLE_PLACES_API_KEY")
    endpoint = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    query = f"{category} in {location}"
    params = {
        "query": query,
        "key": api_key
    }
    response = requests.get(endpoint, params=params)
    data = response.json()
    results = []
    for place in data.get("results", []):
        results.append({
            "name": place.get("name"),
            "address": place.get("formatted_address"),
            "rating": place.get("rating", "N/A"),
        })
    return results 