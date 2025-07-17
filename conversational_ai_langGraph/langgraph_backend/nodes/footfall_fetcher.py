from mock_apis.footfall_mock import get_footfall_data
 
def footfall_fetcher_node(competitors, memory):
    footfall_data = get_footfall_data(competitors)
    memory['footfall'] = footfall_data
    return footfall_data 