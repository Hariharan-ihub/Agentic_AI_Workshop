from mock_apis.google_places_api import search_places

def competitor_search_node(intent_data, memory):
    location = intent_data.get("location")
    category = intent_data.get("category")
    competitors = search_places(location, category)
    memory['competitors'] = competitors
    return competitors