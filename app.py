import streamlit as st
import pandas as pd
from sklearn.cluster import KMeans
import sqlite3
import hashlib
import re

# PAGE SETTINGS
st.set_page_config(
    page_title="Smart Customer Segmentation",
    page_icon="🛍️",
    layout="wide"
)

# DATABASE
def get_database():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS users "
        "(username TEXT PRIMARY KEY, password TEXT NOT NULL)"
    )

    cursor.execute("PRAGMA table_info(users)")
    columns = [row[1] for row in cursor.fetchall()]

    if "email" not in columns:
        cursor.execute(
            "ALTER TABLE users ADD COLUMN email TEXT"
        )

    conn.commit()
    return conn


# PASSWORD HASH
def hash_password(password):
    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


# EMAIL CHECK
def valid_email(email):
    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return re.match(pattern, email) is not None


# CREATE ACCOUNT
def create_account(username, email, password):
    conn = get_database()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT username FROM users WHERE username = ?",
        (username,)
    )

    if cursor.fetchone() is not None:
        conn.close()
        return False

    cursor.execute(
        "INSERT INTO users (username, email, password) "
        "VALUES (?, ?, ?)",
        (
            username,
            email,
            hash_password(password)
        )
    )

    conn.commit()
    conn.close()

    return True


# LOGIN
def login_user(username, password):
    conn = get_database()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT username FROM users "
        "WHERE username = ? AND password = ?",
        (
            username,
            hash_password(password)
        )
    )

    result = cursor.fetchone()

    conn.close()

    return result is not None


get_database().close()


# SESSION
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# ---------------------------------------------------------
# DESIGN
# ---------------------------------------------------------

st.markdown(
    """
    <style>

    .stApp {
        background: linear-gradient(
            135deg,
            #ffd1e8,
            #ffe6f2,
            #fff5fa
        );
        color: #111111;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }

    h1 {
        color: #111111 !important;
        font-size: 42px !important;
        font-weight: 900 !important;
    }

    h2 {
        color: #111111 !important;
        font-size: 32px !important;
        font-weight: 800 !important;
    }

    h3 {
        color: #111111 !important;
        font-size: 25px !important;
        font-weight: 700 !important;
    }

    p {
        color: #111111 !important;
        font-size: 19px !important;
    }

    .title {
        text-align: center;
        font-size: 46px;
        font-weight: 900;
        color: #111111;
        line-height: 1.2;
    }

    .subtitle {
        text-align: center;
        font-size: 21px;
        font-weight: 600;
        color: #222222;
    }

    .card {
        background: #ffffff;
        padding: 25px;
        border-radius: 20px;
        border: 2px solid #111111;
        margin-bottom: 20px;
        box-shadow: 0px 5px 15px rgba(0,0,0,0.12);
    }

    .offer {
        background: #ffffff;
        padding: 25px;
        border-radius: 20px;
        border: 2px solid #111111;
        margin-bottom: 20px;
        box-shadow: 0px 5px 15px rgba(0,0,0,0.12);
    }

    .stButton > button {
        width: 100%;
        min-height: 58px;
        border-radius: 15px;
        background: #111111;
        color: #ffffff;
        border: 2px solid #111111;
        font-size: 19px;
        font-weight: 700;
    }

    .stDownloadButton > button {
        width: 100%;
        min-height: 58px;
        border-radius: 15px;
        background: #111111;
        color: #ffffff;
        border: 2px solid #111111;
        font-size: 19px;
        font-weight: 700;
    }

    .stTextInput input {
        min-height: 52px;
        border-radius: 12px;
        border: 2px solid #111111;
        background: #ffffff;
        color: #111111;
        font-size: 18px;
    }

    [data-testid="stFileUploader"] {
        background: #ffffff;
        padding: 20px;
        border-radius: 18px;
        border: 2px solid #111111;
    }

    @media (max-width: 768px) {

        .block-container {
            padding-left: 0.8rem;
            padding-right: 0.8rem;
        }

        .title {
            font-size: 32px;
        }

        .subtitle {
            font-size: 18px;
        }

        h1 {
            font-size: 30px !important;
        }

        h2 {
            font-size: 26px !important;
        }

        h3 {
            font-size: 22px !important;
        }

        p {
            font-size: 17px !important;
        }

        .card {
            padding: 18px;
        }

        .offer {
            padding: 18px;
        }

        .stButton > button {
            min-height: 62px;
            font-size: 18px;
        }

        .stDownloadButton > button {
            min-height: 62px;
            font-size: 18px;
        }

        .stTextInput input {
            min-height: 56px;
            font-size: 18px;
        }
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# LOGIN PAGE
# =========================================================

if not st.session_state.logged_in:

    st.markdown(
        "<div class='title'>🛍️ Smart Customer Segmentation</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='subtitle'>"
        "Turn customer data into smart business decisions 💡"
        "</div>",
        unsafe_allow_html=True
    )

    st.markdown("---")

    login_tab, signup_tab = st.tabs(
        ["🔐 Login", "📝 Create Account"]
    )

    # LOGIN TAB
    with login_tab:

        st.markdown(
            """
            <div class="card">
            <h2>🔐 Login to Dashboard</h2>
            <p>Enter your account details to continue.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        login_username = st.text_input(
            "👤 Username",
            key="login_username"
        )

        login_password = st.text_input(
            "🔒 Password",
            type="password",
            key="login_password"
        )

        login_clicked = st.button(
            "🚀 Login",
            key="login_button"
        )

        if login_clicked:

            if not login_username.strip():
                st.warning("⚠️ Please enter username.")

            elif not login_password:
                st.warning("⚠️ Please enter password.")

            elif login_user(
                login_username.strip(),
                login_password
            ):

                st.session_state.logged_in = True
                st.success("✅ Login successful!")
                st.rerun()

            else:
                st.error("❌ Invalid username or password.")


    # CREATE ACCOUNT TAB
    with signup_tab:

        st.markdown(
            """
            <div class="card">
            <h2>📝 Create New Account</h2>
            <p>Create an account to use the dashboard.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        new_username = st.text_input(
            "👤 Create Username",
            key="create_username"
        )

        new_email = st.text_input(
            "📧 Email Address",
            key="create_email"
        )

        new_password = st.text_input(
            "🔒 Create Password",
            type="password",
            key="create_password"
        )

        confirm_password = st.text_input(
            "🔒 Confirm Password",
            type="password",
            key="confirm_password"
        )

        signup_clicked = st.button(
            "✨ Create Account",
            key="create_account_button"
        )

        if signup_clicked:

            username = new_username.strip()
            email = new_email.strip()

            if not username:
                st.warning("⚠️ Please enter username.")

            elif not email:
                st.warning("⚠️ Please enter email.")

            elif not valid_email(email):
                st.error("❌ Please enter a valid email.")

            elif not new_password:
                st.warning("⚠️ Please create a password.")

            elif len(new_password) < 4:
                st.warning(
                    "⚠️ Password must contain at least 4 characters."
                )

            elif new_password != confirm_password:
                st.error("❌ Passwords do not match.")

            elif create_account(
                username,
                email,
                new_password
            ):

                st.success(
                    "🎉 Account created successfully!"
                )

                st.info(
                    "Open the Login tab and login with your new account."
                )

            else:
                st.error("❌ Username already exists.")


# =========================================================
# DASHBOARD
# =========================================================

if st.session_state.logged_in:

    st.markdown(
        "<div class='title'>📊 Customer Segmentation Dashboard</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='subtitle'>"
        "Welcome to your Smart Customer Segmentation System! 👋"
        "</div>",
        unsafe_allow_html=True
    )

    st.markdown("---")

    # FEATURE CARDS

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            """
            <div class="card">
            <h2>📁 Upload Dataset</h2>
            <p>
            Upload your customer CSV data
            for analysis.
            </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            """
            <div class="card">
            <h2>🎯 K-Means Groups</h2>
            <p>
            Automatically divide customers
            into four groups.
            </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:

        st.markdown(
            """
            <div class="card">
            <h2>🤖 Smart Offers</h2>
            <p>
            Get marketing ideas for
            different customer groups.
            </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")

    # UPLOAD

    st.subheader("📂 Upload Customer Dataset")

    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=["csv"]
    )

    if uploaded_file is None:

        st.info(
            "👆 Please upload your customer CSV file."
        )

    if uploaded_file is not None:

        try:
            df = pd.read_csv(uploaded_file)

            df.columns = (
                df.columns
                .astype(str)
                .str.strip()
                .str.replace(
                    "\ufeff",
                    "",
                    regex=False
                )
            )

            df = df.reset_index(drop=True)

        except Exception as error:

            st.error(
                "❌ Could not read the CSV file."
            )

            st.write(str(error))

            st.stop()

        st.success(
            "✅ Dataset uploaded successfully!"
        )

        # PREVIEW

        st.subheader("👀 Dataset Preview")

        st.dataframe(
            df,
            use_container_width=True
        )

        st.markdown("---")

        # FIND COLUMNS

        income_column = None
        spending_column = None

        for column in df.columns:

            column_name = (
                str(column)
                .lower()
                .strip()
            )

            if (
                "annual" in column_name
                and "income" in column_name
            ):
                income_column = column

            if (
                "spending" in column_name
                and "score" in column_name
            ):
                spending_column = column

        # COLUMN CHECK

        if (
            income_column is None
            or spending_column is None
        ):

            st.error(
                "❌ Annual Income or Spending Score "
                "column was not found."
            )

            st.write(
                "Columns found in your CSV:"
            )

            st.write(
                list(df.columns)
            )

        if (
            income_column is not None
            and spending_column is not None
        ):

            st.subheader(
                "🎯 Customer Segmentation"
            )

            st.info(
                "The system uses Annual Income "
                "and Spending Score to create "
                "four customer groups."
            )

            run_button = st.button(
                "🚀 Run Customer Segmentation",
                key="run_segmentation"
            )

            if run_button:

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
                        "❌ At least 4 valid customers "
                        "are required."
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

                    # GROUP NAMES

                    df["Customer Group"] = (
                        "Not Available"
                    )

                    for index, cluster in zip(
                        valid_data.index,
                        cluster_numbers
                    ):

                        df.at[
                            index,
                            "Customer Group"
                        ] = (
                            "Group "
                            + str(cluster + 1)
                        )

                    st.success(
                        "🎉 Customer segmentation "
                        "completed successfully!"
                    )

                    # CUSTOMER GROUPS

                    st.subheader(
                        "👥 Customer Groups"
                    )

                    st.dataframe(
                        df,
                        use_container_width=True
                    )

                    # CENTERS

                    centers = model.cluster_centers_

                    average_income = (
                        valid_data[
                            "Income_Value"
                        ].mean()
                    )

                    average_spending = (
                        valid_data[
                            "Spending_Value"
                        ].mean()
                    )

                    # SUMMARY

                    summary_data = []

                    for cluster in range(4):

                        count = int(
                            (
                                cluster_numbers
                                == cluster
                            ).sum()
                        )

                        summary_data.append(
                            {
                                "Group":
                                "Group "
                                + str(cluster + 1),

                                "Customers":
                                count,

                                "Avg Income":
                                round(
                                    centers[
                                        cluster
                                    ][0],
                                    2
                                ),

                                "Avg Spending Score":
                                round(
                                    centers[
                                        cluster
                                    ][1],
                                    2
                                )
                            }
                        )

                    summary_df = pd.DataFrame(
                        summary_data
                    )

                    st.subheader(
                        "📊 Customer Group Summary"
                    )

                    st.dataframe(
                        summary_df,
                        use_container_width=True
                    )

                    # CHART

                    st.subheader(
                        "📈 Customers in Each Group"
                    )

                    chart_data = (
                        summary_df[
                            [
                                "Group",
                                "Customers"
                            ]
                        ]
                        .set_index("Group")
                    )

                    st.bar_chart(
                        chart_data
                    )

                    # IDENTIFY GROUPS

                    vip_group = None
                    potential_group = None
                    deal_group = None
                    growth_group = None

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

                            vip_group = group_name

                        elif (
                            income >= average_income
                            and
                            spending < average_spending
                        ):

                            potential_group = group_name

                        elif (
                            income < average_income
                            and
                            spending >= average_spending
                        ):

                            deal_group = group_name

                        else:

                            growth_group = group_name

                    # SMART INSIGHTS

                    st.subheader(
                        "🤖 Smart Customer Insights"
                    )

                    st.write(
                        "Marketing suggestions based "
                        "on customer income and "
                        "spending behaviour."
                    )

                    st.subheader(
                        "💡 Smart Offers"
                    )

                    # VIP

                    if vip_group is not None:

                        st.markdown(
                            """
                            <div class="offer">
                            <h3>💎 VIP Champions</h3>
                            <p>
                            High income and high spending customers.
                            </p>
                            <p>
                            <b>🎁 Offer:</b>
                            Premium products, loyalty rewards
                            and exclusive early access.
                            </p>
                            <p>
                            <b>📢 Strategy:</b>
                            Build long-term customer loyalty.
                            </p>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    # POTENTIAL

                    if potential_group is not None:

                        st.markdown(
                            """
                            <div class="offer">
                            <h3>🌟 Hidden Potential</h3>
                            <p>
                            High income but lower spending customers.
                            </p>
                            <p>
                            <b>🎁 Offer:</b>
                            Personalised discounts,
                            recommendations and trial offers.
                            </p>
                            <p>
                            <b>📢 Strategy:</b>
                            Encourage more frequent purchases.
                            </p>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    # DEAL LOVERS

                    if deal_group is not None:

                        st.markdown(
                            """
                            <div class="offer">
                            <h3>🔥 Deal Lovers</h3>
                            <p>
                            Lower income but active spending customers.
                            </p>
                            <p>
                            <b>🎁 Offer:</b>
                            Bundle deals, value packs
                            and limited-time offers.
                            </p>
                            <p>
                            <b>📢 Strategy:</b>
                            Reward their engagement.
                            </p>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    # GROWTH

                    if growth_group is not None:

                        st.markdown(
                            """
                            <div class="offer">
                            <h3>🌱 Growth Customers</h3>
                            <p>
                            Lower income and lower spending customers.
                            </p>
                            <p>
                            <b>🎁 Offer:</b>
                            Welcome offers, affordable bundles
                            and first-purchase incentives.
                            </p>
                            <p>
                            <b>📢 Strategy:</b>
                            Encourage first and repeat purchases.
                            </p>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    # DOWNLOAD

                    st.markdown("---")

                    st.subheader(
                        "📥 Download Segmented Customer Report"
                    )

                    download_df = df.drop(
                        columns=[
                            "Income_Value",
                            "Spending_Value"
                        ],
                        errors="ignore"
                    )

                    csv_data = (
                        download_df
                        .to_csv(index=False)
                        .encode("utf-8")
                    )

                    st.download_button(
                        label="📥 Download CSV Report",
                        data=csv_data,
                        file_name="customer_segments.csv",
                        mime="text/csv",
                        key="download_report"
                    )

    # LOGOUT

    st.markdown("---")

    if st.button(
        "🚪 Logout",
        key="logout_button"
    ):

        st.session_state.logged_in = False
        st.rerun()
