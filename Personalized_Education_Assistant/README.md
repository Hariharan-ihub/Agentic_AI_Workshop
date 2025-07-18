# 🎓 Personalized Education Assistant

A Streamlit-based AI-powered assistant that generates personalized learning paths, quizzes, and project ideas for any topic and skill level. Powered by Google Gemini AI and Serper API for up-to-date, high-quality educational content.

---

## 🚀 Features
- **Curated Learning Materials:** Finds top videos, articles, and exercises for your chosen topic.
- **Quiz Generation:** Creates multiple-choice questions to test your understanding.
- **Project Suggestions:** Recommends hands-on projects tailored to your skill level.
- **Easy-to-use Web Interface:** Interactive Streamlit app for instant results.

---

## 🛠️ Requirements
- Python 3.8+
- The following Python packages (see `requirements.txt`):
  - streamlit
  - python-dotenv
  - devtools
  - pydantic
  - requests
  - google-generativeai==0.8.5

---

## 🔑 API Keys Needed
- **Google Gemini API Key** (`GEMINI_API_KEY`)
- **Serper API Key** (`SERPER_API_KEY`)

### How to get them:
- **Gemini API Key:** [Google AI Studio](https://aistudio.google.com/app/apikey)
- **Serper API Key:** [serper.dev](https://serper.dev/)

Create a `.env` file in the project directory with:
```
GEMINI_API_KEY=your_gemini_api_key_here
SERPER_API_KEY=your_serper_api_key_here
```

---

## ⚡ Setup & Run
1. **Clone the repository** (if needed):
   ```sh
   git clone <repo-url>
   cd "Personalized Education Assistant"
   ```
2. **Create and activate a virtual environment (optional but recommended):**
   ```sh
   python -m venv venv
   venv\Scripts\activate  # On Windows
   # or
   source venv/bin/activate  # On macOS/Linux
   ```
3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
4. **Set up your `.env` file** as described above.
5. **Run the app:**
   ```sh
   streamlit run app.py
   ```
6. **Open the app in your browser** (usually at http://localhost:8501 or as shown in the terminal).

---

## 🧪 Sample Topics to Try
- Python Programming (Beginner)
- Machine Learning (Intermediate)
- Data Science (Advanced)
- Web Development (Beginner)
- Cybersecurity (Intermediate)
- Natural Language Processing (Advanced)

---

## 📄 Project Structure
```
Personalized Education Assistant/
├── app.py              # Main Streamlit app
├── requirements.txt    # Python dependencies
├── README.md           # This file
└── .env                # Your API keys (not included in repo)
```

---

## 🤖 Credits
- Powered by [Google Gemini AI](https://ai.google.com/)
- Web search via [Serper API](https://serper.dev/)

---

## 📝 License
This project is for educational and demonstration purposes. 
