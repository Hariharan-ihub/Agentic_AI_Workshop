# Automated Code Debugging Assistant

A Streamlit-based web application that uses CrewAI and LLMs to analyze and automatically fix Python code without executing it. The assistant performs static code analysis, identifies common issues, and suggests or applies corrections, all powered by modern LLMs (e.g., Gemini).

## Features
- **Static Python code analysis** (no code execution)
- **Automatic code correction** for common issues
- **CrewAI multi-agent workflow** (Analyzer, Fixer, Manager)
- **Streamlit web interface** for easy use
- **No ONNX, no chromadb, no code execution**

## Requirements
- Python 3.10+ (tested on 3.13.3)
- [Google Generative AI API key](https://ai.google.dev/)
- See `requirements.txt` for Python dependencies

## Setup Instructions

1. **Clone the repository** and navigate to the project folder:
   ```sh
   cd "Automated code debugging Assistant"
   ```

2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Set your Google API key:**
   - Recommended: Set as an environment variable before running the app:
     - On Windows PowerShell:
       ```powershell
       $env:GOOGLE_API_KEY="your-google-api-key"
       ```
     - On Linux/macOS:
       ```sh
       export GOOGLE_API_KEY="your-google-api-key"
       ```

4. **Run the Streamlit app:**
   ```sh
   streamlit run app.py
   ```
   - If `streamlit` is not recognized, try:
     ```sh
     python -m streamlit run app.py
     ```

## Usage
1. Paste your Python code into the text area.
2. Click **Analyze & Fix**.
3. Review the issues found and the fixed code displayed below.

### Example Test Code
Paste this sample to see the assistant in action:
```python
def divide(a, b):
    try:
        result = a / b
        print("Result is", result)
    except:
        print("An error occurred")

divide(10, 0)
```

## Security Notes
- **Never share your Google API key publicly.**
- For production, always use environment variables for secrets.
- This tool does not execute user code, making it safer for static analysis.

## License
MIT License 
