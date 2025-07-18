# Math-Q&A Agent with LLM and Custom Mathematical Functions

This project is an interactive command-line assistant that can answer general knowledge questions and perform basic math calculations using a Large Language Model (LLM) and custom mathematical tools. It leverages Google Gemini (via LangChain and LangGraph) to provide intelligent, context-aware responses.

---

## Features

- **General Knowledge Q&A:** Ask any question, and the agent will answer using the Gemini LLM.
- **Math Operations:** Supports addition, subtraction, multiplication, and division using custom Python functions as tools.
- **Contextual Chat:** Maintains chat history for more natural, context-aware conversations.
- **Interactive CLI:** Simple command-line interface for easy use.

---

## Requirements

- Python 3.8+
- Google Generative AI (Gemini) API key
- The following Python packages (install via `requirments.txt`):
  - langchain
  - langgraph
  - langchain-google-genai
  - google-generativeai
  - typing-extensions
  - python-dotenv
  - pyautogen

---

## Setup Instructions

1. **Clone the Repository**

   ```sh
   git clone <repo-url>
   cd "Create an Agent using LLM and custom mathematical functions"
   ```

2. **Install Dependencies**

   ```sh
   pip install -r requirments.txt
   ```

3. **Set Up Your Google API Key**

   - Create a `.env` file in this directory with the following content:
     ```
     GOOGLE_API_KEY=your_actual_google_api_key_here
     ```
   - Replace `your_actual_google_api_key_here` with your real API key for Google Generative AI (Gemini).

4. **Run the Agent**

   ```sh
   python math_agent.py
   ```

---

## Usage

- After running the script, you'll see:
  ```
  Math-Q&A Agent ready! Type 'exit' to quit.
  ```
- Type your questions or math problems, for example:
  - `What is 5 + 7?`
  - `Multiply 8 and 12`
  - `Who is the president of France?`
- Type `exit` or `quit` to stop the agent.

---

## Example Interaction

```
Math-Q&A Agent ready! Type 'exit' to quit.

You: What is 15 divided by 3?
Agent: 5.0

You: Who wrote Hamlet?
Agent: William Shakespeare wrote Hamlet.

You: exit
```

---

## Troubleshooting

- **Module Not Found / Import Errors:**
  - Ensure all dependencies are installed with `pip install -r requirments.txt`.
- **API Key Errors:**
  - Make sure your `.env` file is present and contains a valid `GOOGLE_API_KEY`.
- **Python Version Issues:**
  - The code is tested with Python 3.8+. Some dependencies may not yet support Python 3.13.3. If you encounter issues, try Python 3.10 or 3.11.
- **Network Issues:**
  - An internet connection is required for LLM queries.

---

## File Structure

```
math_agent.py         # Main agent script
requirments.txt       # Python dependencies
README.md             # This file
```

---

## License

This project is for educational and research purposes. 
