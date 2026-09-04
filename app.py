
import streamlit as st

st.set_page_config(
    page_title="CustoBloom",
    page_icon="🌸",
    layout="wide"
)

st.title("🌸 CustoBloom")
st.subheader("Smart Customer Segmentation for Smarter Marketing")

st.write("Welcome to the CustoBloom Dashboard! 💗")

st.divider()

col1, col2, col3 = st.columns(3)

col1.metric("👥 Total Customers", "200")
col2.metric("🎯 Customer Segments", "4")
col3.metric("🧠 Algorithm", "K-Means")

st.header("✨ Customer Segments")

st.write("👑 Premium Customers")
st.write("🛍️ Regular Customers")
st.write("💎 High-Income Low Spenders")
st.write("🏷️ Budget Customers")
