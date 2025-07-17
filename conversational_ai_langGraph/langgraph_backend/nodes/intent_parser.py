from langgraph_backend.utils.gemini_llm import gemini_chat
import json

def intent_parser_node(raw_query, memory):
    prompt = f"""
    You are an expert business analyst agent. Extract the following from the user query:
    - intent (e.g., 'analyze competitors')
    - location (e.g., 'Koramangala, Bangalore')
    - category (e.g., 'clothing store')
    Respond in JSON with keys: intent, location, category.
    User query: \"{raw_query}\"
    """
    response = gemini_chat(prompt, max_tokens=200)
    print("Gemini raw response:", response)
    try:
        parsed = json.loads(response)
    except Exception:
        parsed = {"intent": None, "location": None, "category": None}
    memory.update(parsed)
    memory['original_query'] = raw_query
    return parsed