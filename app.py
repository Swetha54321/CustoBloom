import streamlit as st

# Page configuration
st.set_page_config(
    page_title="CustoBloom",
    page_icon="🌸",
    layout="wide"
)

# Login state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# ---------------- LOGIN PAGE ----------------
if not st.session_state.logged_in:

    st.title("🌸 CustoBloom")
    st.subheader("Smart Customer Segmentation for Smarter Marketing")

    st.write("### 🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "admin123":
            st.session_state.logged_in = True
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid username or password.")

    st.info("Demo Login → Username: admin | Password: admin123")


# ---------------- DASHBOARD ----------------
else:

    st.title("🌸 CustoBloom")
    st.subheader("Smart Customer Segmentation for Smarter Marketing")

    st.write("Welcome to the CustoBloom Dashboard! 💗")

    # Logout
    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.rerun()

    st.divider()

    # Dashboard metrics
    col1, col2, col3 = st.columns(3)

    col1.metric("👥 Total Customers", "200")
    col2.metric("🎯 Customer Segments", "4")
    col3.metric("🤖 Algorithm", "K-Means")

    st.header("✨ Customer Segments")

    col1, col2 = st.columns(2)

    with col1:
        st.write("💎 **Premium Customers**")
        st.write("🛍️ **Regular Customers**")

    with col2:
        st.write("💰 **High-Income Low Spenders**")
        st.write("⭐ **Loyal Customers**")

    st.divider()

    st.success("Customer segmentation dashboard is ready!")
