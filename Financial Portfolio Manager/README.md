# 💼 Financial Portfolio Manager

AI-powered personalized investment report generator using Streamlit, AutoGen, and Google Gemini.

---

## 🚀 Overview
This project is a multi-agent financial advisory system that analyzes your investment portfolio and provides personalized recommendations and a comprehensive financial report. It leverages Google Gemini LLM via AutoGen and offers an interactive web interface built with Streamlit.

---

## ✨ Features
- Multi-agent architecture for portfolio analysis, strategy selection, and investment advice
- Supports detailed user input: salary, age, expenses, goals, risk tolerance, and portfolio breakdown
- Generates a professional, actionable financial report in Markdown
- Easy-to-use Streamlit web interface

---

## 🛠️ Setup Instructions

### 1. **Clone the Repository**
```sh
git clone <repo-url>
cd "Financial Portfolio Manager"
```

### 2. **Create and Activate a Virtual Environment**
```sh
python -m venv venv
# Windows:
venv\Scripts\activate
# (or) PowerShell:
venv\Scripts\Activate.ps1
```

### 3. **Install Dependencies**
```sh
pip install -r requirements.txt
pip install "ag2[gemini]"
```

### 4. **Set Up Google Gemini API Key**
- Create a `.env` file in the project directory:
  ```
  GOOGLE_API_KEY=your_actual_gemini_api_key_here
  ```
- Replace `your_actual_gemini_api_key_here` with your real Gemini API key.

### 5. **Run the App**
```sh
streamlit run app.py
```

---

## 📝 Usage
1. Open the app in your browser (usually at http://localhost:8501).
2. Fill in your personal and portfolio details in the form.
3. Click **"Generate Report"**.
4. View your personalized financial report.

---

## 📄 Sample Input

**Personal Details:**
- Annual Salary (₹): 1800000
- Your Age: 28
- Annual Expenses (₹): 600000
- Financial Goals: I want to retire by age 55, buy a second home in 10 years, and fund my child’s higher education in 15 years.
- Risk Tolerance: Moderate

**Portfolio Details:**
- Mutual Funds (Name + Type + Amount):
  ```
  Axis Bluechip Fund - Equity - ₹2,00,000
  HDFC Hybrid Equity Fund - Hybrid - ₹1,00,000
  ```
- Stocks (Name + Qty + Buy Price):
  ```
  Tata Consultancy Services (TCS) - 10 shares - ₹3300
  Infosys - 15 shares - ₹1500
  HDFC Bank - 20 shares - ₹1600
  ```
- Real Estate (Type + Location + Value):
  ```
  2BHK Apartment - Pune - ₹50,00,000 - Rented (₹15,000/month)
  ```
- Fixed Deposit (Total ₹): 500000

---

## 🐞 Troubleshooting
- **Missing Packages:** Install with `pip install <package-name>` as needed.
- **Gemini API Key Error:** Ensure `.env` is present and correctly formatted.
- **Google Gemini/VertexAI Errors:** Run `pip install "ag2[gemini]"`.
- **Port Already in Use:** Change the port with `streamlit run app.py --server.port 8502`.

---

## 🙏 Credits
- [Streamlit](https://streamlit.io/)
- [AutoGen](https://github.com/microsoft/autogen)
- [Google Gemini](https://ai.google.dev/)

---

## 📬 Contact
For questions or support, please open an issue or contact the project maintainer.
