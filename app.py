import streamlit as st
import pandas as pd
from sklearn.cluster import KMeans

# =========================
# PAGE SETTINGS
# =========================

st.set_page_config(
    page_title="Smart Customer Segmentation",
    page_icon="🛍️",
    layout="wide"
)


# =========================
# CUSTOM CSS
# =========================

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
    color: #cbd5e1;
    font-size: 18px;
}

.card {
    background: #1e293b;
    padding: 25px;
    border-radius: 18px;
    border: 1px solid #334155;
    margin-bottom: 15px;
}

.offer {
    background: #172554;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #3b82f6;
    margin-bottom: 12px;
}

</style>
""", unsafe_allow_html=True)


# =========================
# LOGIN STATUS
# =========================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# =========================
# LOGIN PAGE
# =========================

if not st.session_state.logged_in:

    st.markdown(
        "<h1 class='main-title'>🛍️ Smart Customer Segmentation</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p class='subtitle'>Turn customer data into smart business decisions.</p>",
        unsafe_allow_html=True
    )

    st.markdown("---")

    username = st.text_input("👤 Username")

    password = st.text_input(
        "🔒 Password",
        type="password"
    )

    if st.button(
        "🚀 Login",
        use_container_width=True
    ):

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
        "<h1 class='main-title'>📊 Customer Segmentation Dashboard</h1>",
        unsafe_allow_html=True
    )

    st.write(
        "Welcome to our Smart Customer Segmentation System! 👋"
    )

    # -------------------------
    # DASHBOARD CARDS
    # -------------------------

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="card">
        <h2>📁 Upload Dataset</h2>
        <p>Upload your customer CSV data.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">
        <h2>🎯 K-Means Groups</h2>
        <p>Automatically discover customer segments.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="card">
        <h2>🤖 Smart Offers</h2>
        <p>Get targeted marketing suggestions.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")


    # =========================
    # UPLOAD CSV
    # =========================

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

        # Reset index
        df = df.reset_index(drop=True)

        st.success(
            "✅ Dataset uploaded successfully!"
        )


        # =========================
        # DATA PREVIEW
        # =========================

        st.subheader("👀 Dataset Preview")

        st.dataframe(
            df,
            use_container_width=True
        )

        st.markdown("---")


        # =========================
        # FIND REQUIRED COLUMNS
        # =========================

        income_column = None
        spending_column = None


        for column in df.columns:

            name = str(column).lower().strip()

            if "annual" in name and "income" in name:
                income_column = column

            if "spending" in name and "score" in name:
                spending_column = column


        # =========================
        # SEGMENTATION
        # =========================

        if income_column is not None and spending_column is not None:

            st.subheader("🎯 Customer Segmentation")

            if st.button(
                "🚀 Run Customer Segmentation",
                use_container_width=True
            ):

                # Convert data to numbers

                df["Income_Value"] = pd.to_numeric(
                    df[income_column],
                    errors="coerce"
                )

                df["Spending_Value"] = pd.to_numeric(
                    df[spending_column],
                    errors="coerce"
                )


                # Keep valid data

                valid_data = df[
                    ["Income_Value", "Spending_Value"]
                ].dropna()


                if len(valid_data) < 4:

                    st.error(
                        "❌ At least 4 valid customers are required."
                    )

                else:

                    # =========================
                    # K-MEANS
                    # =========================

                    model = KMeans(
                        n_clusters=4,
                        random_state=42,
                        n_init=10
                    )

                    cluster_numbers = model.fit_predict(
                        valid_data
                    )


                    # =========================
                    # CREATE CUSTOMER GROUP
                    # =========================

                    df["Customer Group"] = "Not Available"

                    for index, cluster in zip(
                        valid_data.index,
                        cluster_numbers
                    ):

                        df.at[
                            index,
                            "Customer Group"
                        ] = "Group " + str(cluster + 1)


                    st.success(
                        "🎉 Customer segmentation completed successfully!"
                    )


                    # =========================
                    # CLUSTER CENTERS
                    # =========================

                    centers = model.cluster_centers_


                    # Average income and spending
                    # across all customers

                    average_income = valid_data[
                        "Income_Value"
                    ].mean()

                    average_spending = valid_data[
                        "Spending_Value"
                    ].mean()


                    # =========================
                    # CUSTOMER GROUP RESULTS
                    # =========================

                    st.subheader("👥 Customer Groups")

                    st.dataframe(
                        df.drop(
                            columns=[
                                "Income_Value",
                                "Spending_Value"
                            ]
                        ),
                        use_container_width=True
                    )


                    # =========================
                    # GROUP SUMMARY
                    # =========================

                    st.subheader("📊 Customer Group Summary")

                    summary_data = []

                    for cluster in range(4):

                        cluster_income = centers[cluster][0]

                        cluster_spending = centers[cluster][1]

                        customer_count = (
                            cluster_numbers == cluster
                        ).sum()

                        summary_data.append({
                            "Group":
                                "Group " + str(cluster + 1),

                            "Customers":
                                int(customer_count),

                            "Avg Income":
                                round(cluster_income, 2),

                            "Avg Spending Score":
                                round(cluster_spending, 2)
                        })


                    summary_df = pd.DataFrame(
                        summary_data
                    )

                    st.dataframe(
                        summary_df,
                        use_container_width=True
                    )


                    # =========================
                    # GROUP CHART
                    # =========================

                    st.subheader(
                        "📈 Customers in Each Group"
                    )

                    chart_data = summary_df[
                        ["Group", "Customers"]
                    ].set_index("Group")

                    st.bar_chart(
                        chart_data
                    )


                    # =========================
                    # CUSTOMER BEHAVIOUR
                    # =========================

                    st.markdown("---")

                    st.subheader(
                        "🤖 Smart Customer Insights"
                    )


                    # Find highest/lowest groups

                    high_income_high_spending = None
                    high_income_low_spending = None
                    low_income_high_spending = None
                    low_income_low_spending = None


                    for cluster in range(4):

                        income = centers[cluster][0]
                        spending = centers[cluster][1]

                        group_name = (
                            "Group " + str(cluster + 1)
                        )


                        if (
                            income >= average_income
                            and spending >= average_spending
                        ):

                            high_income_high_spending = (
                                group_name
                            )


                        elif (
                            income >= average_income
                            and spending < average_spending
                        ):

                            high_income_low_spending = (
                                group_name
                            )


                        elif (
                            income < average_income
                            and spending >= average_spending
                        ):

                            low_income_high_spending = (
                                group_name
                            )


                        else:

                            low_income_low_spending = (
                                group_name
                            )


                    # =========================
                    # SMART OFFERS
                    # =========================

                    st.subheader(
                        "💡 Smart Offers & Marketing Ideas"
                    )


                    if high_income_high_spending is not None:

                        st.markdown(
                            f"""
                            <div class="offer">
                            <h3>💎 VIP Champions — {high_income_high_spending}</h3>
                            <p>
                            These customers have high income and high spending behaviour.
                            </p>
                            <b>🎁 Offer:</b>
                            Premium products, loyalty rewards and exclusive early access.
                            <br><br>
                            <b>📢 Strategy:</b>
                            Build long-term loyalty with VIP experiences.
                            </div>
                            """,
                            unsafe_allow_html=True
                        )


                    if high_income_low_spending is not None:

                        st.markdown(
                            f"""
                            <div class="offer">
                            <h3>🌟 Hidden Potential — {high_income_low_spending}</h3>
                            <p>
                            These customers have strong purchasing capacity but lower spending.
                            </p>
                            <b>🎁 Offer:</b>
                            Personalised discounts, product recommendations and trial offers.
                            <br><br>
                            <b>📢 Strategy:</b>
                            Encourage them to increase their purchase frequency.
                            </div>
                            """,
                            unsafe_allow_html=True
                        )


                    if low_income_high_spending is not None:

                        st.markdown(
                            f"""
                            <div class="offer">
                            <h3>🔥 Deal Lovers — {low_income_high_spending}</h3>
                            <p>
                            These customers spend actively despite having lower income.
                            </p>
                            <b>🎁 Offer:</b>
                            Bundle deals, value packs and limited-time offers.
                            <br><br>
                            <b>📢 Strategy:</b>
                            Reward their engagement without reducing product value.
                            </div>
                            """,
                            unsafe_allow_html=True
                        )


                    if low_income_low_spending is not None:

                        st.markdown(
                            f"""
                            <div class="offer">
                            <h3>🌱 Growth Customers — {low_income_low_spending}</h3>
                            <p>
                            These customers currently show lower income and spending.
                            </p>
                            <b>🎁 Offer:</b>
                            Welcome offers, affordable bundles and first-purchase incentives.
                            <br><br>
                            <b>📢 Strategy:</b>
                            Build awareness and encourage repeat purchases.
                            </div>
                            """,
                            unsafe_allow_html=True
                        )


                    # =========================
                    # DOWNLOAD REPORT
                    # =========================

                    st.markdown("---")

                    st.subheader(
                        "📥 Download Segmented Customer Report"
                    )

                    download_df = df.drop(
                        columns=[
                            "Income_Value",
                            "Spending_Value"
                        ]
                    )


                    csv_data = download_df.to_csv(
                        index=False
                    ).encode("utf-8")


                    st.download_button(
                        label="📥 Download CSV Report",
                        data=csv_data,
                        file_name="customer_segments.csv",
                        mime="text/csv",
                        use_container_width=True
                    )


        else:

            st.error(
                "❌ Annual Income or Spending Score column was not found."
            )

            st.write(
                "Columns found in your CSV:"
            )

            st.write(
                list(df.columns)
            )


    # =========================
    # LOGOUT
    # =========================

    st.markdown("---")

    if st.button("🚪 Logout"):

        st.session_state.logged_in = False

        st.rerun()
