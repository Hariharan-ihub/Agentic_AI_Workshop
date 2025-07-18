# Agentic EDA: Streamlining Exploratory Data Analysis with Multi-Agent System using Autogen & Gemini

## Overview
This project demonstrates an automated, agent-based approach to Exploratory Data Analysis (EDA) using Google Gemini and the Autogen multi-agent framework. The system leverages multiple specialized agents to clean data, perform EDA, generate reports, critique results, and validate code—all orchestrated through a user-friendly Streamlit web interface.

## Features
- **Multi-Agent Collaboration:** Data cleaning, EDA, report generation, critique, and code validation by dedicated agents.
- **Google Gemini Integration:** Uses Gemini LLM for natural language processing and code generation.
- **Streamlit UI:** Simple web interface for uploading CSVs and viewing results.
- **Automated Insights:** Generates summary statistics, insights, visual suggestions, and critiques.

## Setup Instructions

### 1. Clone the Repository
```sh
git clone <repo-url>
cd Streamlining_Exploratory_Data_Analysis_with_Multi_Agent_System_using_Autogen
```

### 2. Install Dependencies
Make sure you have Python 3.8+ installed. Then run:
```sh
pip install -r requirements.txt
```

### 3. Set Up Google Gemini API Key
- Obtain your Gemini API key from Google.
- Create a `.env` file in this directory with the following content:
  ```
  GEMINI_API_KEY=your_actual_gemini_api_key_here
  ```
  Replace `your_actual_gemini_api_key_here` with your real key.

### 4. Test the Installation
Run the test script to verify the `autogen-agentchat` package:
```sh
python test.py
```
You should see:
```
✅ AutoGen is working correctly!
```

### 5. Run the Streamlit App
```sh
streamlit run app.py
```
This will open the app in your browser.

## Usage
1. **Upload a CSV file** using the uploader.
2. Click **"🚀 Run Agentic EDA"** to start the analysis.
3. View outputs for:
   - Data preparation code
   - EDA insights
   - Generated EDA report
   - Critic feedback
   - Code validation

## Sample Input
You can use the following sample data. Save it as `sample_data.csv`:

```csv
OrderID,Customer,Product,Quantity,Price,OrderDate
1001,Alice,Widget,5,19.99,2024-01-15
1002,Bob,Gadget,3,29.99,2024-01-16
1003,Charlie,Widget,2,19.99,2024-01-17
1004,Alice,Gizmo,1,49.99,2024-01-18
1005,Bob,Widget,,19.99,2024-01-19
1006,Charlie,Gadget,4,29.99,2024-01-20
1007,Alice,Gizmo,2,,2024-01-21
1008,Bob,Widget,3,19.99,
1009,Charlie,Gizmo,1,49.99,2024-01-23
1010,Alice,Gadget,2,29.99,2024-01-24
```

## Troubleshooting
- **GEMINI_API_KEY not found:** Ensure your `.env` file is present and contains the correct key. Restart your terminal if needed.
- **Missing packages:** Re-run `pip install -r requirements.txt`.
- **App not opening:** Make sure Streamlit is installed and you are in the correct directory.

## License
MIT License

## Acknowledgements
- [Google Gemini](https://ai.google.dev/gemini-api/docs)
- [Autogen](https://github.com/microsoft/autogen)
- [Streamlit](https://streamlit.io/)
