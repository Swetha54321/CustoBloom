import streamlit as st
import pandas as pd
from sklearn.cluster import KMeans

# ---------------- PAGE SETTINGS ----------------

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

.subtitle {
    text-align: center;
    color: #cbd5e1;
    font-size: 18px;
}

.card {
    background: #1e293b;
    padding: 25px;
    border-radius: 18px;
    margin: 10px;
    border: 1px solid #334155;
}

</style>
""", unsafe_allow_html=True)


# ---------------- LOGIN ----------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


if not st.session_state.logged_in:

    st.markdown(
        "<h1 class='main-title'>🛍️ Smart Customer Segmentation</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p class='subtitle'>Login to manage your customer insights</p>",
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


# ---------------- DASHBOARD ----------------

else:

    st.markdown(
        "<h1 class='main-title'>📊 Customer Segmentation Dashboard</h1>",
        unsafe_allow_html=True
    )

    st.write(
        "Welcome to our Smart Customer Segmentation System! 👋"
    )

    # Dashboard cards

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


    # ---------------- CSV UPLOAD ----------------

    st.subheader("📂 Upload Customer Dataset")

    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=["csv"]
    )


    if uploaded_file is not None:

        # Read CSV
        df = pd.read_csv(uploaded_file)

        # Reset index to avoid assignment errors
        df = df.reset_index(drop=True)

        # Clean column names
        df.columns = (
            df.columns
            .astype(str)
            .str.strip()
            .str.replace("\ufeff", "", regex=False)
        )

        st.success("✅ Dataset uploaded successfully!")

        # ---------------- PREVIEW ----------------

        st.subheader("👀 Dataset Preview")

        st.dataframe(
            df,
            use_container_width=True
        )

        st.markdown("---")


        # ---------------- FIND COLUMNS ----------------

        income_column = None
        spending_column = None


        for column in df.columns:

            name = str(column).lower().strip()

            if "annual" in name and "income" in name:
                income_column = column

            if "spending" in name and "score" in name:
                spending_column = column


        # ---------------- SEGMENTATION ----------------

        if income_column is not None and spending_column is not None:

            st.subheader("🎯 Customer Segmentation")

            if st.button(
                "🚀 Run Customer Segmentation",
                use_container_width=True
            ):

                # Convert columns to numbers

                df["Income_Value"] = pd.to_numeric(
                    df[income_column],
                    errors="coerce"
                )

                df["Spending_Value"] = pd.to_numeric(
                    df[spending_column],
                    errors="coerce"
                )


                # Find valid rows

                valid_data = df[
                    ["Income_Value", "Spending_Value"]
                ].dropna()


                if len(valid_data) < 4:

                    st.error(
                        "❌ At least 4 valid customers are required."
                    )

                else:

                    # K-Means model

                    model = KMeans(
                        n_clusters=4,
                        random_state=42,
                        n_init=10
                    )


                    # Create groups

                    group_numbers = model.fit_predict(
                        valid_data
                    ) + 1


                    # Create a new column

                    df["Customer Group"] = "Not Available"


                    # Convert groups to text
                    # This avoids pandas assignment errors

                    group_names = [
                        "Group " + str(number)
                        for number in group_numbers
                    ]


                    # Add groups using matching indexes

                    for index, group in zip(
                        valid_data.index,
                        group_names
                    ):

                        df.at[
                            index,
                            "Customer Group"
                        ] = group


                    # Remove temporary columns

                    df = df.drop(
                        columns=[
                            "Income_Value",
                            "Spending_Value"
                        ]
                    )


                    st.success(
                        "🎉 Customer segmentation completed successfully!"
                    )


                    # ---------------- RESULTS ----------------

                    st.subheader("👥 Customer Groups")

                    st.dataframe(
                        df,
                        use_container_width=True
                    )


                    # ---------------- GROUP SUMMARY ----------------

                    st.subheader("📊 Customer Group Summary")

                    group_count = (
                        df["Customer Group"]
                        .value_counts()
                        .sort_index()
                    )

                    st.bar_chart(group_count)


                    # ---------------- SMART OFFERS ----------------

                    st.markdown("---")

                    st.subheader("💡 Smart Offers")


                    st.info(
                        "🎯 Group 1 – Special discount offers"
                    )

                    st.info(
                        "💎 Group 2 – Premium product offers"
                    )

                    st.info(
                        "🛍️ Group 3 – Personalized offers"
                    )

                    st.info(
                        "🌟 Group 4 – Loyalty and new-product offers"
                    )


        else:

            st.error(
                "❌ Annual Income or Spending Score column was not found."
            )

            st.write("Columns found in your CSV:")

            st.write(list(df.columns))


    # ---------------- LOGOUT ----------------

    st.markdown("---")

    if st.button("🚪 Logout"):

        st.session_state.logged_in = False

        st.rerun()
