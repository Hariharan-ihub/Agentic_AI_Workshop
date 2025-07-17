import streamlit as st
from langgraph_backend.graph import run_graph
from langgraph_backend.memory import get_user_memory
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(page_title="Retail Competitor Analyzer", layout="centered")

st.title("🧾 Retail Competitor Analyzer")
st.write("Ask about competitors in your area (e.g., 'Show me clothing store competitors in Koramangala, Bangalore')")

user_query = st.text_input("Your query:")

if st.button("Analyze") and user_query:
    user_id = st.session_state.get('user_id', 'default')
    memory = get_user_memory(user_id)
    report = run_graph(user_query, memory)
    st.markdown("### 📊 Report")
    st.write(report) 