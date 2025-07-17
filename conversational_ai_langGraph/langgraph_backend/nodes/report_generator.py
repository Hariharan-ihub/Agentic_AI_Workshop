from langgraph_backend.utils.gemini_llm import gemini_chat

def report_generator_node(intent_data, competitors, footfall, insights, memory):
    prompt = f"""
    Create a clear, actionable report for a business owner based on:
    - User query: {intent_data.get('original_query')}
    - Competitors: {competitors}
    - Footfall: {footfall}
    - Strategic insights: {insights}
    Format as a business report.
    """
    report = gemini_chat(prompt, max_tokens=400)
    memory['report'] = report
    return report 