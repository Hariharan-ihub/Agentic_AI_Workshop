from langgraph_backend.utils.gemini_llm import gemini_chat

def strategic_analysis_node(intent_data, competitors, footfall, memory):
    prompt = f"""
    Given the following competitor data and footfall info, provide strategic business insights for a retail clothing store in {intent_data.get('location')}:
    Competitors: {competitors}
    Footfall: {footfall}
    """
    insights = gemini_chat(prompt, max_tokens=300)
    memory['insights'] = insights
    return insights 