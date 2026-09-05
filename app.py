import streamlit as st

# ---------------- PAGE SETTINGS ----------------
st.set_page_config(
    page_title="Customer Segmentation",
    page_icon="🛍️",
    layout="wide"
)

# ---------------- DARK STYLE ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f172a, #172554);
    color: white;
}

.login-box {
    background: rgba(30, 41, 59, 0.95);
    padding: 40px;
    border-radius: 20px;
    max-width: 450px;
    margin: 80px auto;
    box-shadow: 0px 10px 40px rgba(0,0,0,0.4);
}

.title {
    text-align: center;
    font-size: 35px;
    font-weight: bold;
    color: #60a5fa;
}

.subtitle {
    text-align: center;
    color: #cbd5e1;
    margin-bottom: 30px;
}

.dashboard-title {
    font-size: 40px;
    font-weight: bold;
    color: #60a5fa;
}

.card {
    background: rgba(30, 41, 59, 0.9);
    padding: 25px;
    border-radius: 18px;
    margin-top: 20px;
    border: 1px solid #334155;
}
</style>
""", unsafe_allow_html=True)


# ---------------- LOGIN PAGE ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


if not st.session_state.logged_in:

    st.markdown("""
    <div class="login-box">
        <div class="title">🛍️ Smart Customer Segmentation</div>
        <div class="subtitle">
            Login to manage your customer insights
        </div>
    </div>
    """, unsafe_allow_html=True)

    username = st.text_input("👤 Username")
    password = st.text_input("🔒 Password", type="password")

    if st.button("🚀 Login", use_container_width=True):

        if username == "admin" and password == "1234":
            st.session_state.logged_in = True
            st.rerun()

        else:
            st.error("❌ Invalid username or password")


# ---------------- DASHBOARD ----------------
else:

    st.markdown(
        '<div class="dashboard-title">📊 Customer Segmentation Dashboard</div>',
        unsafe_allow_html=True
    )

    st.write("Welcome to your Smart Customer Segmentation System! 👋")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="card">
        <h2>📁 Upload Dataset</h2>
        <p>Upload your customer CSV file.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">
        <h2>🎯 Customer Groups</h2>
        <p>Segment customers using K-Means.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="card">
        <h2>💡 Smart Offers</h2>
        <p>Get offers based on customer groups.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    st.subheader("📂 Upload Customer Dataset")

    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=["csv"]
    )

    if uploaded_file is not None:
        st.success("✅ Dataset uploaded successfully!")

        import pandas as pd

        df = pd.read_csv(uploaded_file)

        st.subheader("👀 Dataset Preview")
        st.dataframe(df)

    st.markdown("---")

    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.rerun()
