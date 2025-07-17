from langgraph_backend.nodes.intent_parser import intent_parser_node
from langgraph_backend.nodes.competitor_search import competitor_search_node
from langgraph_backend.nodes.footfall_fetcher import footfall_fetcher_node
from langgraph_backend.nodes.strategic_analysis import strategic_analysis_node
from langgraph_backend.nodes.report_generator import report_generator_node
from langgraph_backend.logger import log_phase

def run_graph(user_query, memory):
    # 1. Intent parsing
    intent_data = intent_parser_node(user_query, memory)
    print("Intent Data:", intent_data)
    # 2. Competitor search
    competitors = competitor_search_node(intent_data, memory)
    print("Competitors:", competitors)
    # 3. Footfall fetch
    footfall = footfall_fetcher_node(competitors, memory)
    print("Footfall:", footfall)
    # 4. Strategic analysis
    insights = strategic_analysis_node(intent_data, competitors, footfall, memory)
    # 5. Report generation
    report = report_generator_node(intent_data, competitors, footfall, insights, memory)
    return report 