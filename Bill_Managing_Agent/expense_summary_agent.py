

def summarize_expenses(categorized_data):
    total = sum(categorized_data.values())
    max_category = max(categorized_data, key=categorized_data.get)

    summary = {
        "Total": total,
        "Highest Category": max_category,
        "Details": categorized_data
    }

    return summary
