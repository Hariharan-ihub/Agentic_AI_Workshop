from PIL import Image
import pytesseract

# Optional: Set tesseract path manually (Windows)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

def extract_text_from_image(image_path):
    """Extract raw text from an image using Tesseract OCR"""
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    print("OCR Output:", repr(text))  # Debug print
    return text
