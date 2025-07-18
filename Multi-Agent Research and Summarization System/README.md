# 🧾 Multi Agent Bill Management System

A smart bill management app that uses OCR and multi-agent processing to extract, categorize, and summarize spending from uploaded bill images. Built with Python and Streamlit.

## Features
- Upload bill images (JPG, PNG)
- Automatic OCR extraction of items and prices
- Categorizes spending (Groceries, Dining, Utilities, Entertainment, Shopping)
- Visual spending summary and category breakdown
- Bar chart visualization

## Requirements
- Python 3.8+
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- pip (Python package manager)

## Setup

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd Multi_agent_billing_system
```

### 2. Create and Activate a Virtual Environment (Recommended)
```bash
python -m venv env
# On Windows:
env\Scripts\activate
# On Mac/Linux:
source env/bin/activate
```

### 3. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 4. Install Tesseract OCR
- **Windows:**
  - Download the installer from [UB Mannheim builds](https://github.com/UB-Mannheim/tesseract/wiki).
  - Install to the default location (e.g., `C:\Program Files\Tesseract-OCR`).
  - Ensure the path is set in `utils/ocr_utils.py`:
    ```python
    pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
    ```
- **Mac:**
  ```bash
  brew install tesseract
  ```
- **Linux:**
  ```bash
  sudo apt-get install tesseract-ocr
  ```

### 5. Run the App
```bash
streamlit run app.py
```
- Open the provided local URL in your browser.

## Usage
1. Click **Upload Bill Image** and select a bill image file.
2. Click **Process Bill**.
3. View the categorized spending summary and bar chart.

## Project Structure
```
Multi_agent_billing_system/
├── app.py                  # Streamlit app UI
├── bill_processing_agent.py# OCR and categorization logic
├── expense_summary_agent.py# Summarization logic
├── group_manager.py        # Orchestrates agents
├── utils/
│   └── ocr_utils.py        # OCR utility functions
└── sample_bills/           # Uploaded bill images (auto-created)
```

## Troubleshooting
- **TesseractNotFoundError:**
  - Ensure Tesseract is installed and the path is set in `ocr_utils.py`.
  - Restart your terminal/IDE after installation.
- **OCR accuracy issues:**
  - Use clear, high-contrast images.
  - Edit `bill_processing_agent.py` to improve parsing logic if needed.

## License
MIT 
