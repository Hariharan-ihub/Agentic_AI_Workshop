# 🧠 Multi-Agent Research and Summarization System

A fully agentic research assistant that combines Retrieval-Augmented Generation (RAG), Web Search, and Large Language Model (LLM) capabilities using LangGraph, Gemini (Google Generative AI), and Streamlit. Upload your own documents for custom Q&A, or ask general research questions and get concise, summarized answers.

---

## 🚀 Features
- **Multi-Agent Workflow:** Routes queries to Web Search, RAG, or LLM based on intent.
- **Document Q&A:** Upload `.pdf`, `.txt`, or `.docx` files to the `my_docs/` folder for custom retrieval.
- **Web Search Integration:** Uses DuckDuckGo for up-to-date information.
- **Summarization:** All answers are summarized for clarity and brevity.
- **Streamlit UI:** Simple, interactive web interface.

---

## 🛠️ Setup Instructions

### 1. **Clone the Repository**
```
git clone <repo-url>
cd "Multi-Agent Research and Summarization System"
```

### 2. **Install Dependencies**
```
pip install -r requirements.txt
```

### 3. **Set Up Google API Key**
- Get your API key from [Google AI Studio](https://makersuite.google.com/) or Google Cloud Console.
- Set the key as an environment variable:
  - **Windows (PowerShell):**
    ```powershell
    $env:GOOGLE_API_KEY="your-key-here"
    ```
  - **Linux/Mac:**
    ```bash
    export GOOGLE_API_KEY="your-key-here"
    ```
  - Or create a `.env` file in the project directory:
    ```
    GOOGLE_API_KEY=your-key-here
    ```

### 4. **(Optional) Add Documents**
- Place any `.pdf`, `.txt`, or `.docx` files you want to query in the `my_docs/` folder.

### 5. **Run the App**
```
python -m streamlit run app.py
```
- The app will open in your browser.

---

## 💡 Usage
1. Enter your question in the input box (e.g., "What is LangGraph?").
2. Click **Submit**.
3. The system will route your query, retrieve and summarize the answer, and display it.

---

## 📝 Sample Questions
- What is LangGraph and how is it used in AI workflows?
- Who developed the Gemini 1.5 Flash model?
- Summarize the contents of the file "dataSet.pdf".
- What are the key findings in my uploaded document?
- Compare the capabilities of Gemini 1.5 Flash and GPT-4.
- How does retrieval-augmented generation (RAG) improve question answering?

---

## 🔄 Sample Workflow
1. User uploads documents to `my_docs/` (optional).
2. User asks a question in the app.
3. The router agent classifies the query (web, rag, llm).
4. The appropriate agent fetches/generates an answer.
5. The summarizer agent condenses the answer.
6. The answer is displayed in the app.

---

## 🛠️ Troubleshooting
- **streamlit: command not found**
  - Use `python -m streamlit run app.py` instead, or add your Python Scripts directory to PATH.
- **GOOGLE_API_KEY not found**
  - Make sure your API key is set as an environment variable or in a `.env` file.
- **No documents loaded**
  - Ensure your files are in the `my_docs/` folder and are readable (`.pdf`, `.txt`, `.docx`).
- **Other errors**
  - Check the terminal for error messages and ensure all dependencies are installed.

---

## 📄 License
MIT License (or specify your license here)
