
import streamlit as st
import json
import autogen
from autogen import AssistantAgent, UserProxyAgent


import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')  
if not api_key:
    raise ValueError("Gemini API key missing!")


config_list_gemini = [{
    "model": "gemini-2.5-flash",
    "api_key": api_key,
    "api_type": "google"
}]


st.title("💼 Financial Portfolio Manager")
st.markdown("AI-powered personalized investment report")

with st.form("financial_form"):
    salary = st.text_input("Annual Salary (₹)", placeholder="1200000")
    age = st.number_input("Your Age", min_value=18, max_value=100, step=1)
    expenses = st.text_input("Annual Expenses (₹)", placeholder="500000")
    goals = st.text_area("Financial Goals", placeholder="Retirement in 20 years, buying a home in 5 years")
    risk = st.selectbox("Risk Tolerance", ["Conservative", "Moderate", "Aggressive"])

    st.subheader("🪙 Portfolio Details")
    mutual_funds = st.text_area("Mutual Funds (Name + Type + Amount)", placeholder="Axis Bluechip - Equity - ₹2L")
    stocks = st.text_area("Stocks (Name + Qty + Buy Price)", placeholder="Infosys - 10 shares - ₹1500")
    real_estate = st.text_area("Real Estate (Type + Location + Value)", placeholder="Residential Apartment - Mumbai - ₹10L")
    fixed_deposit = st.text_input("Fixed Deposit (Total ₹)", placeholder="500000")

    submit = st.form_submit_button("Generate Report")


portfolio_analyst = AssistantAgent(
    name="PortfolioAnalyst",
    llm_config={"config_list": config_list_gemini},
    system_message="""
    Analyze the user's portfolio and determine investment strategy. 
    Output ONLY in JSON format: {"strategy": "Growth" or "Value", "reason": "brief explanation"}
    """
)

growth_strategist = AssistantAgent(
    name="GrowthStrategist",
    llm_config={"config_list": config_list_gemini},
    system_message="""
    Suggest high-growth investments: mid-cap mutual funds, global ETFs, tech stocks, or crypto.
    Output: {"recommendations": ["item1", "item2", ...], "rationale": "brief explanation"}
    """
)

value_strategist = AssistantAgent(
    name="ValueStrategist",
    llm_config={"config_list": config_list_gemini},
    system_message="""
    Suggest stable investments: bonds, blue-chip stocks, or government schemes.
    Output: {"recommendations": ["item1", "item2", ...], "rationale": "brief explanation"}
    """
)

financial_advisor = AssistantAgent(
    name="FinancialAdvisor",
    llm_config={"config_list": config_list_gemini},
    system_message="""
    Compile a comprehensive financial report with:
    1. Portfolio Analysis Summary
    2. Recommended Strategy
    3. Specific Investment Recommendations
    4. Implementation Plan
    5. Risk Assessment
    Format the report in Markdown. Add "TERMINATE" at the end when done.
    """
)

user_proxy = UserProxyAgent(
    name="UserProxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=5,
    is_termination_msg=lambda x: "TERMINATE" in x.get("content", ""),
    code_execution_config=False
)

def extract_strategy(content):
    try:
        data = json.loads(content.strip())
        return data.get("strategy", "Growth")
    except:
        return "Growth"


def manage_investment_portfolio():
    message = f"""
User Profile:
- Age: {age}
- Annual Salary: ₹{salary}
- Annual Expenses: ₹{expenses}
- Risk Tolerance: {risk}
- Financial Goals: {goals}

Current Portfolio:
- Mutual Funds: {mutual_funds or 'None'}
- Stocks: {stocks or 'None'}
- Real Estate: {real_estate or 'None'}
- Fixed Deposit: ₹{fixed_deposit or '0'}
"""

    # Step 1: Portfolio Analysis
    analysis_result = user_proxy.initiate_chat(
        portfolio_analyst,
        message=message,
        summary_method="last_msg",
        silent=True
    )
    analysis_summary = analysis_result.chat_history[-1]["content"]
    strategy = extract_strategy(analysis_summary)

    # Step 2: Get Recommendations
    agent = growth_strategist if strategy == "Growth" else value_strategist
    recommendations_result = user_proxy.initiate_chat(
        agent,
        message=f"{message}\nStrategy: {strategy}",
        summary_method="last_msg",
        silent=True
    )
    recommendations_summary = recommendations_result.chat_history[-1]["content"]

    # Step 3: Generate Final Report
    report_result = user_proxy.initiate_chat(
        financial_advisor,
        message=f"""
Generate a comprehensive financial report based on:

User Profile:
{message}

Portfolio Analysis:
{analysis_summary}

Investment Recommendations:
{recommendations_summary}

Include these sections:
1. Portfolio Analysis Summary
2. Recommended Strategy
3. Specific Investment Recommendations
4. Implementation Plan
5. Risk Assessment
""",
        summary_method="last_msg",
        silent=True
    )

    # Extract the actual report content
    report_content = report_result.chat_history[-1]["content"]
    if "TERMINATE" in report_content:
        return report_content.split("TERMINATE")[0].strip()
    return report_content

# ⏳ Generate and Display
if submit:
    with st.spinner("🧠 Analyzing your portfolio... This may take 1-2 minutes"):
        try:
            result = manage_investment_portfolio()
            st.subheader("📊 Your Personalized Financial Report")
            st.markdown(result)
        except Exception as e:
            st.error(f"Error generating report: {str(e)}")
            st.info("Please check your inputs and try again. If the problem persists, try reducing the amount of text in your inputs.")
