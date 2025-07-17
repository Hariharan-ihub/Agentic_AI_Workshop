def get_footfall_data(competitors):
    # Mocked data; in real use, call a footfall analytics API
    return [
        {"store": c["name"], "estimated_footfall": 1200 + i*100, "busiest_hours": "5-8pm"}
        for i, c in enumerate(competitors)
    ] 