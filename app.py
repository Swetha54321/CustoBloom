import streamlit as st
import pandas as pd
from sklearn.cluster import KMeans
import sqlite3
import hashlib
import re


# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="Smart Customer Segmentation",
    page_icon="🛍️",
    layout="wide"
)


# =========================================================
# DATABASE
# =========================================================

def create_database():

    conn = sqlite3.connect("users.db")

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def hash_password(password):

    return hashlib.sha256(
        password.encode()
    ).hexdigest()


def valid_email(email):

    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

    return re.match(pattern, email) is not None


def register_user(username, email, password):

    conn = sqlite3.connect("users.db")

    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO users
            (username, email, password)
            VALUES (?, ?, ?)
            """,
            (
                username,
                email,
                hash_password(password)
            )
        )

        conn.commit()

        success = True

    except sqlite3.IntegrityError:

        success = False

    conn.close()

    return success


def check_login(username, password):

    conn = sqlite3.connect("users.db")

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE username = ?
        AND password = ?
        """,
        (
            username,
            hash_password(password)
        )
    )

    user = cursor.fetchone()

    conn.close()

    return user is not None


create_database()


# =========================================================
# SESSION STATE
# =========================================================

if "logged_in" not in st.session_state:

    st.session_state.logged_in = False


# =========================================================
# CUSTOM CSS
# =========================================================

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


# =========================================================
# LOGIN / SIGN UP PAGE
# =========================================================

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

    login_tab, signup_tab = st.tabs(
        ["🔐 Login", "📝 Create Account"]
    )


    # =====================================================
    # LOGIN
    # =====================================================

    with login_tab:

        st.subheader("🔐 Login to Dashboard")

        username = st.text_input(
            "👤 Username",
            key="login_username"
        )

        password = st.text_input(
            "🔒 Password",
            type="password",
            key="login_password"
        )

        if st.button(
            "🚀 Login",
            use_container_width=True
        ):

            if (
                username.strip() == ""
                or password.strip() == ""
            ):

                st.warning(
                    "⚠️ Please enter username and password."
                )

            elif check_login(
                username.strip(),
                password
            ):

                st.session_state.logged_in = True

                st.success(
                    "✅ Login successful!"
                )

                st.rerun()

            else:

                st.error(
                    "❌ Invalid username or password."
                )


    # =====================================================
    # CREATE ACCOUNT
    # =====================================================

    with signup_tab:

        st.subheader("📝 Create New Account")

        new_username = st.text_input(
            "👤 Create Username",
            key="signup_username"
        )

        new_email = st.text_input(
            "📧 Email Address",
            key="signup_email"
        )

        new_password = st.text_input(
            "🔒 Create Password",
            type="password",
            key="signup_password"
        )

        confirm_password = st.text_input(
            "🔒 Confirm Password",
            type="password",
            key="confirm_password"
        )

        if st.button(
            "✨ Create Account",
            use_container_width=True
        ):

            username_clean = new_username.strip()

            email_clean = new_email.strip()

            if (
                username_clean == ""
                or email_clean == ""
                or new_password == ""
                or confirm_password == ""
            ):

                st.warning(
                    "⚠️ Please fill all fields."
                )

            elif not valid_email(email_clean):

                st.error(
                    "❌ Please enter a valid email address."
                )

            elif len(new_password) < 4:

                st.warning(
                    "⚠️ Password should contain at least 4 characters."
                )

            elif new_password != confirm_password:

                st.error(
                    "❌ Passwords do not match."
                )

            else:

                created = register_user(
                    username_clean,
                    email_clean,
                    new_password
                )

                if created:

                    st.success(
                        "🎉 Account created successfully! "
                        "You can now login."
                    )

                else:

                    st.error(
                        "❌ Username already exists. "
                        "Please choose another username."
                    )


# =========================================================
# DASHBOARD
# =========================================================

else:

    st.markdown(
        "<h1 class='main-title'>📊 Customer Segmentation Dashboard</h1>",
        unsafe_allow_html=True
    )

    st.write(
        "Welcome to your Smart Customer Segmentation System! 👋"
    )

    st.markdown("---")


    # =====================================================
    # TOP CARDS
    # =====================================================

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


    # =====================================================
    # UPLOAD DATASET
    # =====================================================

    st.subheader("📂 Upload Customer Dataset")

    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=["csv"]
    )


    if uploaded_file is not None:

        df = pd.read_csv(uploaded_file)

        df.columns = (
            df.columns
            .astype(str)
            .str.strip()
            .str.replace("\ufeff", "", regex=False)
        )

        df = df.reset_index(drop=True)

        st.success(
            "✅ Dataset uploaded successfully!"
        )


        # =================================================
        # DATASET PREVIEW
        # =================================================

        st.subheader("👀 Dataset Preview")

        st.dataframe(
            df,
            use_container_width=True
        )

        st.markdown("---")


        # =================================================
        # FIND REQUIRED COLUMNS
        # =================================================

        income_column = None

        spending_column = None


        for column in df.columns:

            name = str(column).lower().strip()

            if (
                "annual" in name
                and "income" in name
            ):

                income_column = column

            if (
                "spending" in name
                and "score" in name
            ):

                spending_column = column


        # =================================================
        # CUSTOMER SEGMENTATION
        # =================================================

        if (
            income_column is not None
            and spending_column is not None
        ):

            st.subheader(
                "🎯 Customer Segmentation"
            )

            if st.button(
                "🚀 Run Customer Segmentation",
                use_container_width=True
            ):

                df["Income_Value"] = pd.to_numeric(
                    df[income_column],
                    errors="coerce"
                )

                df["Spending_Value"] = pd.to_numeric(
                    df[spending_column],
                    errors="coerce"
                )

                valid_data = df[
                    [
                        "Income_Value",
                        "Spending_Value"
                    ]
                ].dropna()


                if len(valid_data) < 4:

                    st.error(
                        "❌ At least 4 valid customers are required."
                    )

                else:

                    # K-MEANS

                    model = KMeans(
                        n_clusters=4,
                        random_state=42,
                        n_init=10
                    )

                    cluster_numbers = model.fit_predict(
                        valid_data
                    )


                    # GROUP ASSIGNMENT

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


                    # =================================================
                    # CUSTOMER GROUPS
                    # =================================================

                    st.subheader(
                        "👥 Customer Groups"
                    )

                    st.dataframe(
                        df,
                        use_container_width=True
                    )


                    # =================================================
                    # CLUSTER CENTERS
                    # =================================================

                    centers = model.cluster_centers_

                    average_income = valid_data[
                        "Income_Value"
                    ].mean()

                    average_spending = valid_data[
                        "Spending_Value"
                    ].mean()


                    # =================================================
                    # GROUP SUMMARY
                    # =================================================

                    st.subheader(
                        "📊 Customer Group Summary"
                    )

                    summary_data = []


                    for cluster in range(4):

                        cluster_income = centers[
                            cluster
                        ][0]

                        cluster_spending = centers[
                            cluster
                        ][1]

                        customer_count = (
                            cluster_numbers == cluster
                        ).sum()


                        summary_data.append({

                            "Group":
                                "Group "
                                + str(cluster + 1),

                            "Customers":
                                int(customer_count),

                            "Avg Income":
                                round(
                                    cluster_income,
                                    2
                                ),

                            "Avg Spending Score":
                                round(
                                    cluster_spending,
                                    2
                                )
                        })


                    summary_df = pd.DataFrame(
                        summary_data
                    )


                    st.dataframe(
                        summary_df,
                        use_container_width=True
                    )


                    # =================================================
                    # BAR CHART
                    # =================================================

                    st.subheader(
                        "📈 Customers in Each Group"
                    )

                    chart_data = summary_df[
                        [
                            "Group",
                            "Customers"
                        ]
                    ].set_index("Group")


                    st.bar_chart(
                        chart_data
                    )


                    st.markdown("---")


                    # =================================================
                    # SMART INSIGHTS
                    # =================================================

                    st.subheader(
                        "🤖 Smart Customer Insights"
                    )


                    high_income_high_spending = None

                    high_income_low_spending = None

                    low_income_high_spending = None

                    low_income_low_spending = None


                    for cluster in range(4):

                        income = centers[
                            cluster
                        ][0]

                        spending = centers[
                            cluster
                        ][1]

                        group_name = (
                            "Group "
                            + str(cluster + 1)
                        )


                        if (
                            income >= average_income
                            and
                            spending >= average_spending
                        ):

                            high_income_high_spending = (
                                group_name
                            )

                        elif (
                            income >= average_income
                            and
                            spending < average_spending
                        ):

                            high_income_low_spending = (
                                group_name
                            )

                        elif (
                            income < average_income
                            and
                            spending >= average_spending
                        ):

                            low_income_high_spending = (
                                group_name
                            )

                        else:

                            low_income_low_spending = (
                                group_name
                            )


                    # =================================================
                    # SMART OFFERS
                    # =================================================

                    st.subheader(
                        "💡 Smart Offers & Marketing Ideas"
                    )


                    if high_income_high_spending is not None:

                        st.markdown(
                            f"""
                            <div class="offer">

                            <h3>
                            💎 VIP Champions —
                            {high_income_high_spending}
                            </h3>

                            <p>
                            These customers have high income
                            and high spending behaviour.
                            </p>

                            <b>🎁 Offer:</b>
                            Premium products, loyalty rewards
                            and exclusive early access.

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

                            <h3>
                            🌟 Hidden Potential —
                            {high_income_low_spending}
                            </h3>

                            <p>
                            These customers have strong purchasing
                            capacity but lower spending.
                            </
