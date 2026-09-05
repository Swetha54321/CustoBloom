import streamlit as st
import pandas as pd
from sklearn.cluster import KMeans

# PAGE SETTINGS
st.set_page_config(
    page_title="Smart Customer Segmentation",
    page_icon="🛍️",
    layout="wide"
)

# STYLE
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f172a, #172554);
    color: white;
}

.title {
    text-align: center;
    font-size: 38px;
    font-weight: bold;
    color: #60a5fa;
}

.subtitle {
    text-align: center;
    color: #cbd5e1;
    font-size: 18px;
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


# LOGIN STATUS
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# =========================
# LOGIN PAGE
# =========================

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

    password = st.text_input(
        "🔒 Password",
        type="password"
    )

    if st.button("🚀 Login", use_container_width=True):

        if username == "admin" and password == "1234":

            st.session_state.logged_in = True
            st.rerun()

        else:

            st.error("❌ Invalid username or password")


# =========================
# DASHBOARD
# =========================

else:

    st.markdown(
        '<div class="dashboard-title">'
        '📊 Customer Segmentation Dashboard'
        '</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Welcome to our Smart Customer Segmentation System! 👋"
    )


    # DASHBOARD CARDS

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


    # =========================
    # UPLOAD DATASET
    # =========================

    st.subheader("📂 Upload Customer Dataset")

    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=["csv"]
    )


    if uploaded_file is not None:

        try:

            df = pd.read_csv(uploaded_file)

            # Remove extra spaces from column names
            df.columns = df.columns.str.strip()

            st.success(
                "✅ Dataset uploaded successfully!"
            )


            # DATA PREVIEW

            st.subheader("👀 Dataset Preview")

            st.dataframe(
                df,
                use_container_width=True
            )


            # =========================
            # SEGMENTATION
            # =========================

            st.markdown("---")

            st.subheader("🎯 Customer Segmentation")


            # Check columns

            required_columns = [
                "Annual Income",
                "Spending Score"
            ]


            missing_columns = [
                column
                for column in required_columns
                if column not in df.columns
            ]


            if len(missing_columns) > 0:

                st.error(
                    "❌ Required columns are missing."
                )

                st.write(
                    "Columns found in your dataset:"
                )

                st.write(
                    list(df.columns)
                )


            else:

                if st.button(
                    "🚀 Run Customer Segmentation",
                    use_container_width=True
                ):

                    # Select features

                    X = df[
                        [
                            "Annual Income",
                            "Spending Score"
                        ]
                    ].copy()


                    # Convert values to numbers

                    X["Annual Income"] = pd.to_numeric(
                        X["Annual Income"],
                        errors="coerce"
                    )

                    X["Spending Score"] = pd.to_numeric(
                        X["Spending Score"],
                        errors="coerce"
                    )


                    # Remove empty values

                    valid_rows = X.dropna().index

                    X_clean = X.loc[valid_rows]


                    if len(X_clean) < 4:

                        st.error(
                            "❌ Not enough valid customer data "
                            "to create 4 groups."
                        )

                    else:

                        # K-MEANS MODEL

                        kmeans = KMeans(
                            n_clusters=4,
                            random_state=42,
                            n_init=10
                        )


                        # Create groups

                        groups = kmeans.fit_predict(
                            X_clean
                        ) + 1


                        # Add groups to original dataframe

                        df["Customer Group"] = "Not Available"

                        df.loc[
                            valid_rows,
                            "Customer Group"
                        ] = groups


                        st.success(
                            "🎉 Customer segmentation "
                            "completed successfully!"
                        )


                        # SHOW GROUPS

                        st.subheader(
                            "👥 Customer Groups"
                        )

                        st.dataframe(
                            df,
                            use_container_width=True
                        )


                        # GROUP COUNT

                        st.subheader(
                            "📊 Group Summary"
                        )

                        group_counts = (
                            df["Customer Group"]
                            .value_counts()
                            .sort_index()
                        )

                        st.bar_chart
