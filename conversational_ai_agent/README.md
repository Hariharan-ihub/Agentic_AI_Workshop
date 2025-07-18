# Clothing Store Competitor Intelligence

This project is a Streamlit web application that provides AI-powered competitor analysis for clothing stores in any location. It leverages Google Gemini (via LangChain) for advanced analysis and the Google Places API for real-world competitor data. Optionally, it can use autogen-agentchat for multi-agent workflows.

## Features
- Fetches real clothing store data from Google Places API
- Analyzes competitors using Google Gemini (LLM)
- Generates business-ready, downloadable reports
- User-friendly Streamlit interface

## Setup & Installation

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd <project-directory>
```

### 2. Create and activate a virtual environment (recommended)
```bash
python -m venv myenv
# On Windows:
myenv\Scripts\activate
# On Mac/Linux:
source myenv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```
If you don't have a requirements.txt, install manually:
```bash
pip install streamlit langchain-google-genai langchain-core requests
# For autogen-agentchat (optional, for multi-agent version):
pip install autogen-agentchat
```

### 4. Set up API Keys
- **Google Gemini API Key:** Get from [Google AI Studio](https://aistudio.google.com/app/apikey)
- **Google Places API Key:** Get from [Google Cloud Console](https://console.cloud.google.com/apis/library/places-backend.googleapis.com)

You will enter these keys in the app sidebar when running the app.

## Usage
```bash
streamlit run app.py
```
- Enter your API keys and location in the sidebar.
- Click "Fetch Competitors" to get real store data.
- Click "Generate Analysis" to get a detailed report.
- Download the report as a markdown file.

## Troubleshooting
- **Dependency Conflicts:**
  - If you see errors about `pillow` or `protobuf` versions, try:
    ```bash
    pip install --upgrade "pillow<11" "protobuf>=5.29.3,<6.0.0"
    ```
  - If you use autogen-agentchat, you may need `pillow>=11` (which conflicts with Streamlit <1.33). Consider using the latest Streamlit version if possible.
- **ModuleNotFoundError:**
  - Ensure you are in the correct virtual environment and all dependencies are installed.
- **API Errors:**
  - Double-check your API keys and quota in Google Cloud Console.

## .gitignore
See the included `.gitignore` file for recommended exclusions.

## License
MIT License 
