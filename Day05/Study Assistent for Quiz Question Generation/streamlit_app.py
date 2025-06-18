import streamlit as st
from assessment_generator import AssessmentGenerator
import time

st.set_page_config(page_title="Quiz Assessment Generator", layout="centered")
st.title("📚 Quiz Assessment Generator (Gemini)")

st.write("""
Paste or upload educational content below. The app will summarize the content and generate multiple-choice quiz questions using Google's Gemini AI (gemini-1.5-flash).
""")

# Initialize session state for storing results
if 'assessment_result' not in st.session_state:
    st.session_state.assessment_result = None

# Text input
content = st.text_area("Paste your educational content here:", height=200)

# File upload
uploaded_file = st.file_uploader("Or upload a .txt file:", type=["txt"])

if uploaded_file is not None:
    file_content = uploaded_file.read().decode("utf-8")
    content = file_content
    st.success("File uploaded and loaded!")

if st.button("Generate Assessment"):
    if not content.strip():
        st.warning("Please provide some educational content.")
    else:
        try:
            with st.spinner("Generating Summary and Questions..."):
                generator = AssessmentGenerator()
                result = generator.generate_assessment(content)
                st.session_state.assessment_result = result
                
            # Display Summary
            st.subheader("📝 Summary")
            for point in result["summary"]:
                st.markdown(f"- {point}")
            
            # Display Questions
            st.subheader("❓ Quiz Questions")
            for idx, q in enumerate(result["questions"], 1):
                with st.container():
                    st.markdown(f"**Question {idx}:** {q['question']}")
                    for opt in q["options"]:
                        st.markdown(f"- {opt}")
                    with st.expander("Show Answer"):
                        st.markdown(f"**Correct Answer:** {q['correct_answer']}")
                    st.markdown("---")
                
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.info("Please try again with different content or check your API key.")

# Add a clear button
if st.button("Clear Results"):
    st.session_state.assessment_result = None
    st.experimental_rerun() 