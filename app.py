import streamlit as st
import pandas as pd
from sklearn.cluster import KMeans

st.set_page_config(
    page_title="Smart Customer Segmentation",
    page_icon="🛍️",
    layout="wide"
)

# ---------------- STYLE ----------------

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f172a, #172554);
    color: white;
}

.main-title {
    font-size: 40px;
    font-weight: bold;
    color: #60a5fa;
}

.card {
    background: #1e293b;
    padding: 25px;
    border-radius: 18px;
    margin: 10px;
}
</style>
""", unsafe_allow_html=True)


# ---------------- LOGIN ----------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


if st.session_state.logged_in == False:

    st.markdown(
        "<h1 class='main-title'>🛍️ Smart Customer Segmentation</h1>",
        unsafe_allow_html=True
    )

    st.write("Login to manage your customer insights")

    username = st.text_input("👤 Username")
    password = st.text_input("🔒 Password", type="password")

    if st.button("🚀 Login"):

        if username == "admin" and password == "1234":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("❌ Invalid username or password")


# ---------------- DASHBOARD ----------------

else:

    st.markdown(
        "<h1 class='main-title'>📊 Customer Segmentation Dashboard</h1>",
        unsafe_allow_html=True
    )

    st.write(
        "Welcome to our Smart Customer Segmentation System! 👋"
    )

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

    # ---------------- UPLOAD ----------------

    st.subheader("📂 Upload Customer Dataset")

    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=["csv"]
    )

    if uploaded_file is not None:

        df = pd.read_csv(uploaded_file)

        df.columns = df.columns.str.strip()

        st.success("✅ Dataset uploaded successfully!")

        st.subheader("👀 Dataset Preview")

        st.dataframe(
            df,
            use_container_width=True
        )

        st.markdown("---")

        # ---------------- CHECK COLUMNS ----------------

        if "Annual Income" in df.columns and "Spending Score" in df.columns:

            st.subheader("🎯 Customer Segmentation")

            if st.button(
                "🚀 Run Customer Segmentation",
                use_container_width=True
            ):

                income = pd.to_numeric(
                    df["Annual Income"],
                    errors="coerce"
                )

                spending = pd.to_numeric(
                    df["Spending Score"],
                    errors="coerce"
                )

                data = pd.DataFrame({
                    "Annual Income": income,
                    "Spending Score": spending
                })

                data = data.dropna()

                if len(data) >= 4:

                    model = KMeans(
                        n_clusters=4,
                        random_state=42,
                        n_init=10
                    )

                    groups = model.fit_predict(data)

                    df["Customer Group"] = "Not Available"

                    df.loc[
                        data.index,
                        "Customer Group"
                    ] = groups + 1

                    st.success(
                        "🎉 Customer segmentation completed successfully!"
                    )

                    st.subheader("👥 Customer Groups")

                    st.dataframe(
                        df,
                        use_container_width=True
                    )

                    st.subheader("📊 Group Summary")

                    group_count = df[
                        "Customer Group"
                    ].value_counts().sort_index()

                    st.bar_chart(group_count)

                    st.markdown("---")

                    st.subheader("💡 Smart Offers")

                    st.info(
                        "🎯 Group 1: Special discount offers"
                    )

                    st.info(
                        "💎 Group 2: Premium product offers"
                    )

                    st.info(
                        "🛍️ Group 3: Personalized offers"
                    )

                    st.info(
                        "🌟 Group 4: Loyalty and new-product offers"
                    )

                else:

                    st.error(
                        "❌ Not enough valid customer data."
                    )

        else:

            st.error(
                "❌ Annual Income or Spending Score column is missing."
            )

            st.write("Columns found in your CSV:")

            st.write(list(df.columns))

    st.markdown("---")

    if st.button("🚪 Logout"):

        st.session_state.logged_in = False

        st.rerun()
