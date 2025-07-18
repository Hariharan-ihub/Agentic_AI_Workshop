import streamlit as st
from group_manager import process_bill
import matplotlib.pyplot as plt

st.set_page_config(page_title="🧾 Bill Management Agent", layout="centered")

st.title("🧾 Smart Bill Management Agent")
st.write("Upload your bill image and get categorized spending summary!")

uploaded_file = st.file_uploader("Upload Bill Image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    with open(f"sample_bills/{uploaded_file.name}", "wb") as f:
        f.write(uploaded_file.read())

    st.success("Image Uploaded Successfully!")

    if st.button("Process Bill"):
        summary = process_bill(f"sample_bills/{uploaded_file.name}")

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
