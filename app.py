import streamlit as st
import pandas as pd
from sklearn.cluster import KMeans

# Page settings
st.set_page_config(
    page_title="Smart Customer Segmentation",
    page_icon="🛍️",
    layout="wide"
)

# Login status
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# =========================
# LOGIN PAGE
# =========================

if not st.session_state.logged_in:

    st.title("🛍️ Smart Customer Segmentation")

    st.write("Login to manage your customer insights")

    username = st.text_input("👤 Username")

    password = st.text_input(
        "🔒 Password",
        type="password"
    )

    if st.button("🚀 Login"):

        if username == "admin" and password == "1234":

            st.session_state.logged_in = True
            st.rerun()

        else:

            st.error("❌ Invalid username or password")


# =========================
# DASHBOARD
# =========================

else:

    st.title("📊 Customer Segmentation Dashboard")

    st.write(
        "Welcome to our Smart Customer Segmentation System! 👋"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("📁 Upload Dataset")

    with col2:
        st.info("🎯 Customer Groups")

    with col3:
        st.info("💡 Smart Offers")

    st.markdown("---")

    # Upload CSV
    st.subheader("📂 Upload Customer Dataset")

    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=["csv"]
    )

    if uploaded_file is not None:

        df = pd.read_csv(uploaded_file)

        # Clean column names
        df.columns = (
            df.columns
            .astype(str)
            .str.strip()
            .str.replace("\ufeff", "", regex=False)
        )

        st.success("✅ Dataset uploaded successfully!")

        st.subheader("👀 Dataset Preview")

        st.dataframe(
            df,
            use_container_width=True
        )

        st.markdown("---")

        # Show columns
        st.write("Columns found in your CSV:")

        st.write(list(df.columns))

        # Find Annual Income column
        income_column = None

        for column in df.columns:

            column_name = str(column).lower().strip()

            if "annual" in column_name and "income" in column_name:
                income_column = column


        # Find Spending Score column
        spending_column = None

        for column in df.columns:

            column_name = str(column).lower().strip()

            if "spending" in column_name and "score" in column_name:
                spending_column = column


        # Check columns
        if income_column is not None and spending_column is not None:

            st.subheader("🎯 Customer Segmentation")

            if st.button(
                "🚀 Run Customer Segmentation",
                use_container_width=True
            ):

                income = pd.to_numeric(
                    df[income_column],
                    errors="coerce"
                )

                spending = pd.to_numeric(
                    df[spending_column],
                    errors="coerce"
                )

                data = pd.DataFrame({
                    "Income": income,
                    "Spending": spending
                })

                data = data.dropna()

                if len(data) >= 4:

                    # K-Means
                    model = KMeans(
                        n_clusters=4,
                        random_state=42,
                        n_init=10
                    )

                    groups = model.fit_predict(data)

                    # Add groups
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

                    # Group summary
                    st.subheader("📊 Customer Group Summary")

                    group_count = (
                        df["Customer Group"]
                        .value_counts()
                        .sort_index()
                    )

                    st.bar_chart(group_count)

                    # Smart offers
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
                        "❌ Not enough valid customer data."
                    )

        else:

            st.error(
                "❌ Required columns could not be identified."
            )


    # Logout
    st.markdown("---")

    if st.button("🚪 Logout"):

        st.session_state.logged_in = False

        st.rerun()
