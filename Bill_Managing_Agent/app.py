import streamlit as st
from group_manager import process_bill
import matplotlib.pyplot as plt
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAMPLE_BILLS_DIR = os.path.join(BASE_DIR, "sample_bills")
os.makedirs(SAMPLE_BILLS_DIR, exist_ok=True)

st.set_page_config(page_title="🧾 Bill Management Agent", layout="centered")

st.title("🧾 Smart Bill Management Agent")
st.write("Upload your bill image and get categorized spending summary!")

uploaded_file = st.file_uploader("Upload Bill Image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    file_path = os.path.join(SAMPLE_BILLS_DIR, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    st.success("Image Uploaded Successfully!")

    if st.button("Process Bill"):
        summary = process_bill(file_path)

        st.subheader("📊 Spending Summary")
        st.write(f"**Total Expenditure**: ₹{summary['Total']}")
        st.write(f"**Highest Spending Category**: {summary['Highest Category']}")

        st.subheader("🔍 Category Breakdown")
        st.json(summary["Details"])

        # Plotting
        fig, ax = plt.subplots()
        categories = list(summary["Details"].keys())
        values = list(summary["Details"].values())
        ax.bar(categories, values, color="skyblue")
        plt.xticks(rotation=45)
        st.pyplot(fig)
