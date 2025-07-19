

from bill_processing_agent import extract_and_categorize
from expense_summary_agent import summarize_expenses
import pytesseract

# Add this line (update the path if your install is different)
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

def process_bill(image_path):
    categorized_data = extract_and_categorize(image_path)
    summary = summarize_expenses(categorized_data)
    return summary
