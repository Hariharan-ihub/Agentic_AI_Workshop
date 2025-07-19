

from utils.ocr_utils import extract_text_from_image
import re

def extract_and_categorize(image_path):
    text = extract_text_from_image(image_path)
    lines = [line.strip() for line in text.split('\n') if line.strip()]

    categories = {
        "Groceries": 0,
        "Dining": 0,
        "Utilities": 0,
        "Entertainment": 0,
        "Shopping": 0
    }

    i = 0
    while i < len(lines) - 1:
        item_line = lines[i]
        price_line = lines[i + 1]

        # Try to parse price
        try:
            price = int(''.join(filter(str.isdigit, price_line)))
        except ValueError:
            i += 1
            continue

        item = item_line.lower()
        if any(word in item for word in ["milk", "rice", "vegetable"]):
            categories["Groceries"] += price
        elif any(word in item for word in ["burger", "pizza", "restaurant"]):
            categories["Dining"] += price
        elif any(word in item for word in ["electric", "gas", "water"]):
            categories["Utilities"] += price
        elif any(word in item for word in ["movie", "game", "ticket"]):
            categories["Entertainment"] += price
        else:
            categories["Shopping"] += price

        i += 2  # Move to next item-price pair

    return categories
