# Legal & Compliance Risk Identifier

This application helps analyze business models and identify potential legal and compliance risks using AI-powered agents. It uses Streamlit for the frontend and LangChain for the AI framework.

## Features

- Business Model Analysis: Identifies business domain and geographical scope
- Risk Detection: Analyzes potential legal and compliance risks
- RAG (Retrieval-Augmented Generation) capabilities for improved accuracy
- Support for both text input and document upload

## Setup

1. Clone this repository
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the root directory with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Running the Application

1. Start the Streamlit application:
   ```bash
   streamlit run app.py
   ```
2. Open your browser and navigate to the URL shown in the terminal (typically http://localhost:8501)

## Usage

1. Choose your input method (Text Input or File Upload)
2. Enter your business description or upload a document
3. Click "Analyze Business Model and Risks"
4. View the analysis results for both business model and potential risks

## Architecture

The application consists of two main agents:

1. **Business Model Analyzer Agent**
   - Determines business domain and geographical scope
   - Uses RAG to check for similar existing analyses
   - Provides structured output with justification

2. **Risk Detection Agent**
   - Identifies legal and compliance risks
   - Considers domain-specific regulations
   - Provides detailed risk profiles with relevant laws and descriptions

## Vector Store

The application uses FAISS for vector storage and similarity search. The vector store is automatically initialized when the application starts and persists between sessions.

## Contributing

Feel free to submit issues and enhancement requests! 