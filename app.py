import streamlit as st
import pandas as pd
from sklearn.cluster import KMeans

# ---------------- PAGE SETTINGS ----------------
st.set_page_config(
    page_title="Smart Customer Segmentation",
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


# ---------------- LOGIN STATUS ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# ==================================================
# LOGIN PAGE
# ==================================================

if not st.session_state.logged_in:

    st.markdown(
        '<div class="title">🛍️ Smart Customer Segmentation</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Login to manage your customer insights</div>',
        unsafe_allow_html=True
    )

    username = st.text_input("👤 Username")
    password = st.text_input("🔒 Password", type="password")

    if st.button("🚀 Login", use_container_width=True):

        if username == "admin" and password == "1234":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("❌ Invalid username or password")


# ==================================================
# DASHBOARD
# ==================================================

else:

    st.markdown(
        '<div class="dashboard-title">📊 Customer Segmentation Dashboard</div>',
        unsafe_allow_html=True
    )

    st.write("Welcome to our Smart Customer Segmentation System! 👋")

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

    # ---------------- UPLOAD DATASET ----------------

    st.subheader("📂 Upload Customer Dataset")

    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=["csv"]
    )

    if uploaded_file is not None:

        df = pd.read_csv(uploaded_file)

        st.success("✅ Dataset uploaded successfully!")

        st.subheader("👀 Dataset Preview")
        st.dataframe(df)

        # ---------------- K-MEANS ----------------

        st.markdown("---")

        st.subheader("🎯 Customer Segmentation")

        if st.button(
            "🚀 Run Customer Segmentation",
            use_container_width=True
        ):

            # Select columns for K-Means
            X = df[["Annual Income", "Spending Score"]]

            # Create K-Means model
            kmeans = KMeans(
                n_clusters=4,
                random_state=42,
                n_init=10
            )

            # Predict customer groups
            df["Customer Group"] = kmeans.fit_predict(X) + 1

            st.success(
                "🎉 Customer segmentation completed successfully!"
            )

            st.subheader("👥 Customer Groups")

            st.dataframe(df)

            st.info(
                "Customers have been divided into 4 groups "
                "based on Annual Income and Spending Score."
            )

    # ---------------- LOGOUT ----------------

    st.markdown("---")

    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.rerun()
