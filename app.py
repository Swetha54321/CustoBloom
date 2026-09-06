import streamlit as st
import pandas as pd
from sklearn.cluster import KMeans
import sqlite3
import hashlib
import re

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="Smart Customer Segmentation",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------
# DATABASE
# ---------------------------------------------------------
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
        cursor.execute("ALTER TABLE users ADD COLUMN email TEXT")

    conn.commit()
    return conn


def hash_password(password):
    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


def valid_email(email):
    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return re.match(pattern, email) is not None


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
        "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
        (username, email, hash_password(password))
    )

    conn.commit()
    conn.close()

    return True


def login_user(username, password):
    conn = get_database()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT username FROM users "
        "WHERE username = ? AND password = ?",
        (username, hash_password(password))
    )

    result = cursor.fetchone()

    conn.close()

    return result is not None


get_database().close()

# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "auth_page" not in st.session_state:
    st.session_state.auth_page = "login"

# ---------------------------------------------------------
# PROFESSIONAL DARK BLUE UI
# ---------------------------------------------------------
st.markdown(
    """
    <style>

    /* ---------- GLOBAL ---------- */

    .stApp {
        background: #071426;
        color: #ffffff;
        font-family: Arial, Helvetica, sans-serif;
    }

    [data-testid="stAppViewContainer"] {
        background: #071426;
    }

    [data-testid="stHeader"] {
        background: #071426;
    }

    .block-container {
        max-width: 1180px;
        padding-top: 35px;
        padding-bottom: 50px;
    }

    /* ---------- REMOVE EXTRA STREAMLIT SPACE ---------- */

    h1, h2, h3, p {
        font-family: Arial, Helvetica, sans-serif;
    }

    /* ---------- MAIN TITLE ---------- */

    .main-title {
        text-align: center;
        font-family: "Trebuchet MS", Arial, sans-serif;
        font-size: 48px;
        font-weight: 800;
        letter-spacing: 0.5px;
        color: #ffffff;
        margin-top: 20px;
        margin-bottom: 10px;
    }

    .main-subtitle {
        text-align: center;
        font-size: 18px;
        color: #b9c7d9;
        margin-bottom: 35px;
    }

    /* ---------- AUTH LAYOUT ---------- */

    .brand-area {
        text-align: center;
        padding: 20px 10px 30px 10px;
    }

    .brand-icon {
        font-size: 58px;
        margin-bottom: 10px;
    }

    .brand-title {
        font-family: "Trebuchet MS", Arial, sans-serif;
        font-size: 44px;
        font-weight: 800;
        color: #ffffff;
        line-height: 1.15;
    }

    .brand-title span {
        color: #5ec8ff;
    }

    .brand-description {
        color: #aebdd0;
        font-size: 17px;
        line-height: 1.6;
        max-width: 560px;
        margin: 18px auto 0 auto;
    }

    .feature-box {
        background: #0d2038;
        border: 1px solid #1c3958;
        border-radius: 16px;
        padding: 18px;
        margin-top: 15px;
        color: #d8e3ef;
    }

    .feature-box b {
        color: #ffffff;
    }

    /* ---------- LOGIN CARD ---------- */

    [data-testid="stForm"] {
        background: #ffffff !important;
        border: 1px solid #d8e0e8 !important;
        border-radius: 20px !important;
        padding: 30px !important;
        box-shadow: 0 15px 45px rgba(0, 0, 0, 0.35) !important;
    }

    .login-heading {
        color: #0b1b2d;
        font-family: "Trebuchet MS", Arial, sans-serif;
        font-size: 30px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .login-subheading {
        color: #657487;
        font-size: 14px;
        margin-bottom: 20px;
    }

    /* ---------- INPUTS ---------- */

    [data-testid="stWidgetLabel"] p {
        color: #172536 !important;
        font-weight: 600 !important;
    }

    input {
        color: #172536 !important;
        background: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 10px !important;
    }

    input:focus {
        border: 1px solid #2296d2 !important;
        box-shadow: 0 0 0 2px rgba(34, 150, 210, 0.15) !important;
    }

    /* ---------- BUTTONS ---------- */

    .stButton > button,
    .stFormSubmitButton > button {
        border-radius: 10px !important;
        border: none !important;
        min-height: 45px !important;
        font-weight: 700 !important;
        background: #168acb !important;
        color: #ffffff !important;
    }

    .stButton > button:hover,
    .stFormSubmitButton > button:hover {
        background: #0f70aa !important;
        color: #ffffff !important;
    }

    /* ---------- AUTH SWITCH ---------- */

    .switch-text {
        text-align: center;
        color: #64748b;
        font-size: 14px;
        margin-top: 15px;
        margin-bottom: 4px;
    }

    /* ---------- DASHBOARD CARDS ---------- */

    .dashboard-card {
        background: #0d2038;
        border: 1px solid #1c3958;
        border-radius: 16px;
        padding: 22px;
        min-height: 150px;
    }

    .dashboard-card h3 {
        color: #ffffff;
        margin-bottom: 8px;
    }

    .dashboard-card p {
        color: #aebdd0;
        line-height: 1.5;
    }

    /* ---------- OFFER CARDS ---------- */

    .offer-card {
        background: #0d2038;
        border: 1px solid #285071;
        border-radius: 16px;
        padding: 22px;
        margin-bottom: 16px;
    }

    .offer-card h3 {
        color: #ffffff;
        margin-bottom: 8px;
    }

    .offer-card p {
        color: #c1cfdd;
        line-height: 1.55;
    }

    .offer-label {
        color: #5ec8ff;
        font-weight: 700;
    }

    /* ---------- SECTION TITLES ---------- */

    .section-title {
        color: #ffffff;
        font-family: "Trebuchet MS", Arial, sans-serif;
        font-size: 28px;
        font-weight: 800;
        margin-top: 30px;
        margin-bottom: 15px;
    }

    /* ---------- MOBILE ---------- */

    @media (max-width: 768px) {

        .block-container {
            padding: 18px 14px 35px 14px;
        }

        .main-title {
            font-size: 32px;
            line-height: 1.2;
        }

        .main-subtitle {
            font-size: 15px;
            margin-bottom: 25px;
        }

        .brand-title {
            font-size: 32px;
        }

        .brand-description {
            font-size: 15px;
        }

        .brand-icon {
            font-size: 45px;
        }

        [data-testid="stForm"] {
            padding: 20px !important;
            border-radius: 16px !important;
        }

        .login-heading {
            font-size: 25px;
        }

        .dashboard-card {
            margin-bottom: 12px;
            min-height: auto;
        }

        .section-title {
            font-size: 24px;
        }
    }

    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# LOGIN / CREATE ACCOUNT PAGE
# =========================================================

if not st.session_state.logged_in:

    left, right = st.columns([1.25, 0.9], gap="large")

    # -----------------------------------------------------
    # LEFT SIDE
    # -----------------------------------------------------

    with left:

        st.markdown(
            """
            <div class="brand-area">

                <div class="brand-icon">🛍️</div>

                <div class="brand-title">
                    Smart Customer<br>
                    <span>Segmentation</span>
                </div>

                <div class="brand-description">
                    Transform customer data into meaningful
                    business insights using machine learning
                    and intelligent customer grouping.
                </div>

                <div class="feature-box">
                    <b>🎯 Customer Segmentation</b><br>
                    Discover meaningful customer groups
                    using K-Means clustering.
                </div>

                <div class="feature-box">
                    <b>📊 Data Analysis</b><br>
                    Understand customer income and
                    spending behaviour.
                </div>

                <div class="feature-box">
                    <b>💡 Smart Marketing</b><br>
                    Get targeted offers and marketing
                    strategies for each customer group.
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    # -----------------------------------------------------
    # RIGHT SIDE
    # -----------------------------------------------------

    with right:

        if st.session_state.auth_page == "login":

            with st.form("login_form"):

                st.markdown(
                    "<div class='login-heading'>Sign In</div>",
                    unsafe_allow_html=True
                )

                st.markdown(
                    "<div class='login-subheading'>"
                    "Sign in to access your dashboard"
                    "</div>",
                    unsafe_allow_html=True
                )

                username = st.text_input(
                    "Username",
                    placeholder="Enter your username"
                )

                password = st.text_input(
                    "Password",
                    type="password",
                    placeholder="Enter your password"
                )

                login_clicked = st.form_submit_button(
                    "SIGN IN  →",
                    use_container_width=True
                )

                if login_clicked:

                    if username.strip() == "" or password == "":
                        st.warning(
                            "Please enter username and password."
                        )

                    elif login_user(
                        username.strip(),
                        password
                    ):
                        st.session_state.logged_in = True
                        st.rerun()

                    else:
                        st.error(
                            "Invalid username or password."
                        )

            st.markdown(
                "<div class='switch-text'>"
                "Don't have an account?"
                "</div>",
                unsafe_allow_html=True
            )

            if st.button(
                "CREATE ACCOUNT",
                use_container_width=True
            ):
                st.session_state.auth_page = "signup"
                st.rerun()

        # -------------------------------------------------
        # CREATE ACCOUNT
        # -------------------------------------------------

        else:

            with st.form("signup_form"):

                st.markdown(
                    "<div class='login-heading'>Create Account</div>",
                    unsafe_allow_html=True
                )

                st.markdown(
                    "<div class='login-subheading'>"
                    "Create an account to use the system"
                    "</div>",
                    unsafe_allow_html=True
                )

                new_username = st.text_input(
                    "Username",
                    placeholder="Create a username"
                )

                new_email = st.text_input(
                    "Email",
                    placeholder="Enter your email address"
                )

                new_password = st.text_input(
                    "Password",
                    type="password",
                    placeholder="Create a password"
                )

                confirm_password = st.text_input(
                    "Confirm Password",
                    type="password",
                    placeholder="Confirm your password"
                )

                create_clicked = st.form_submit_button(
                    "CREATE ACCOUNT  →",
                    use_container_width=True
                )

                if create_clicked:

                    username_value = new_username.strip()
                    email_value = new_email.strip()

                    if (
                        username_value == ""
                        or email_value == ""
                        or new_password == ""
                        or confirm_password == ""
                    ):
                        st.warning(
                            "Please fill all the fields."
                        )

                    elif not valid_email(email_value):
                        st.error(
                            "Please enter a valid email address."
                        )

                    elif len(new_password) < 4:
                        st.warning(
                            "Password must contain at least 4 characters."
                        )

                    elif new_password != confirm_password:
                        st.error(
                            "Passwords do not match."
                        )

                    else:

                        created = create_account(
                            username_value,
                            email_value,
                            new_password
                        )

                        if created:
                            st.success(
                                "Account created successfully!"
                            )
                            st.session_state.auth_page = "login"

                        else:
                            st.error(
                                "Username already exists."
                            )

            st.markdown(
                "<div class='switch-text'>"
                "Already have an account?"
                "</div>",
                unsafe_allow_html=True
            )

            if st.button(
                "SIGN IN",
                use_container_width=True
            ):
                st.session_state.auth_page = "login"
                st.rerun()


# =========================================================
# DASHBOARD
# =========================================================

else:

    st.markdown(
        "<div class='main-title'>"
        "🛍️ Smart Customer Segmentation"
        "</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='main-subtitle'>"
        "Analyse customer behaviour and discover meaningful segments"
        "</div>",
        unsafe_allow_html=True
    )

    st.markdown("---")

    # -----------------------------------------------------
    # FEATURE CARDS
    # -----------------------------------------------------

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            """
            <div class="dashboard-card">
                <h3>📁 Upload Dataset</h3>
                <p>
                Upload your customer CSV dataset
                and preview the available data.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            """
            <div class="dashboard-card">
                <h3>🎯 K-Means Analysis</h3>
                <p>
                Automatically divide customers
                into four meaningful groups.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            """
            <div class="dashboard-card">
                <h3>💡 Smart Offers</h3>
                <p>
                Generate marketing ideas based
                on customer behaviour.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")

    # -----------------------------------------------------
    # UPLOAD
    # -----------------------------------------------------

    st.markdown(
        "<div class='section-title'>📁 Upload Customer Dataset</div>",
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=["csv"]
    )

    if uploaded_file is not None:

        df = pd.read_csv(uploaded_file)

        df.columns = (
            df.columns.astype(str)
            .str.strip()
            .str.replace("\ufeff", "", regex=False)
        )

        df = df.reset_index(drop=True)

        st.success(
            "Dataset uploaded successfully!"
        )

        st.markdown(
            "<div class='section-title'>👀 Dataset Preview</div>",
            unsafe_allow_html=True
        )

        st.dataframe(
            df,
            use_container_width=True
        )

        income_column = None
        spending_column = None

        for column in df.columns:

            column_name = str(column).lower().strip()

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

        # -------------------------------------------------
        # SEGMENTATION
        # -------------------------------------------------

        if (
            income_column is not None
            and spending_column is not None
        ):

            st.markdown(
                "<div class='section-title'>"
                "🎯 Customer Segmentation"
                "</div>",
                unsafe_allow_html=True
            )

            if st.button(
                "🚀 RUN CUSTOMER SEGMENTATION",
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
                    ["Income_Value", "Spending_Value"]
                ].dropna()

                if len(valid_data) < 4:

                    st.error(
                        "At least 4 valid customers are required."
                    )

                else:

                    model = KMeans(
                        n_clusters=4,
                        random_state=42,
                        n_init=10
                    )

                    cluster_numbers = model.fit_predict(
                        valid_data
                    )

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
                        "Customer segmentation completed successfully!"
                    )

                    # -------------------------------------
                    # CUSTOMER GROUPS
                    # -------------------------------------

                    st.markdown(
                        "<div class='section-title'>"
                        "👥 Customer Groups"
                        "</div>",
                        unsafe_allow_html=True
                    )

                    st.dataframe(
                        df,
                        use_container_width=True
                    )

                    # -------------------------------------
                    # SUMMARY
                    # -------------------------------------

                    centers = model.cluster_centers_

                    average_income = (
                        valid_data["Income_Value"].mean()
                    )

                    average_spending = (
                        valid_data["Spending_Value"].mean()
                    )

                    summary_data = []

                    for cluster in range(4):

                        income = centers[cluster][0]
                        spending = centers[cluster][1]

                        count = (
                            cluster_numbers == cluster
                        ).sum()

                        summary_data.append(
                            {
                                "Group":
                                    "Group " + str(cluster + 1),
                                "Customers":
                                    int(count),
                                "Avg Income":
                                    round(income, 2),
                                "Avg Spending Score":
                                    round(spending, 2)
                            }
                        )

                    summary_df = pd.DataFrame(
                        summary_data
                    )

                    st.markdown(
                        "<div class='section-title'>"
                        "📊 Customer Group Summary"
                        "</div>",
                        unsafe_allow_html=True
                    )

                    st.dataframe(
                        summary_df,
                        use_container_width=True
                    )

                    # -------------------------------------
                    # BAR CHART
                    # -------------------------------------

                    st.markdown(
                        "<div class='section-title'>"
                        "📈 Customers in Each Group"
                        "</div>",
                        unsafe_allow_html=True
                    )

                    chart_data = (
                        summary_df[
                            ["Group", "Customers"]
                        ]
                        .set_index("Group")
                    )

                    st.bar_chart(chart_data)

                    # -------------------------------------
                    # SEMANTIC GROUPS
                    # -------------------------------------

                    vip_group = None
                    potential_group = None
                    deal_group = None
                    growth_group = None

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
                            vip_group = group_name

                        elif (
                            income >= average_income
                            and spending < average_spending
                        ):
                            potential_group = group_name

                        elif (
                            income < average_income
                            and spending >= average_spending
                        ):
                            deal_group = group_name

                        else:
                            growth_group = group_name

                    # -------------------------------------
                    # SMART INSIGHTS
                    # -------------------------------------

                    st.markdown(
                        "<div class='section-title'>"
                        "💡 Smart Customer Insights"
                        "</div>",
                        unsafe_allow_html=True
                    )

                    if vip_group is not None:

                        st.markdown(
                            """
                            <div class="offer-card">
                                <h3>💎 VIP Champions</h3>
                                <p>
                                High income and high spending customers.
                                </p>
                                <p>
                                <span class="offer-label">
                                🎁 Recommended Offer:
                                </span>
                                Premium products, loyalty rewards
                                and exclusive early access.
                                </p>
                                <p>
                                <span class="offer-label">
                                📢 Strategy:
                                </span>
                                Build long-term customer loyalty.
                                </p>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    if potential_group is not None:

                        st.markdown(
                            """
                            <div class="offer-card">
                                <h3>🌟 Hidden Potential</h3>
                                <p>
                                High income but lower spending customers.
                                </p>
                                <p>
                                <span class="offer-label">
                                🎁 Recommended Offer:
                                </span>
                                Personalised discounts,
                                recommendations and trial offers.
                                </p>
                                <p>
                                <span class="offer-label">
                                📢 Strategy:
                                </span>
                                Encourage more frequent purchases.
                                </p>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    if deal_group is not None:

                        st.markdown(
                            """
                            <div class="offer-card">
                                <h3>🔥 Deal Lovers</h3>
                                <p>
                                Lower income but active spending customers.
                                </p>
                                <p>
                                <span class="offer-label">
                                🎁 Recommended Offer:
                                </span>
                                Bundle deals, value packs
                                and limited-time offers.
                                </p>
                                <p>
                                <span class="offer-label">
                                📢 Strategy:
                                </span>
                                Reward their engagement.
                                </p>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    if growth_group is not None:

                        st.markdown(
                            """
                            <div class="offer-card">
                                <h3>🌱 Growth Customers</h3>
                                <p>
                                Lower income and lower spending customers.
                                </p>
                                <p>
                                <span class="offer-label">
                                🎁 Recommended Offer:
                                </span>
                                Welcome offers, affordable bundles
                                and first-purchase incentives.
                                </p>
                                <p>
                                <span class="offer-label">
                                📢 Strategy:
                                </span>
                                Encourage first and repeat purchases.
                                </p>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    # -------------------------------------
                    # DOWNLOAD
                    # -------------------------------------

                    st.markdown(
                        "<div class='section-title'>"
                        "📥 Download Segmented Report"
                        "</div>",
                        unsafe_allow_html=True
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
                        label="📥 DOWNLOAD CSV REPORT",
                        data=csv_data,
                        file_name="customer_segments.csv",
                        mime="text/csv",
                        use_container_width=True
                    )

        else:

            st.error(
                "Annual Income or Spending Score column was not found."
            )

            st.write(
                "Columns found in your CSV:"
            )

            st.write(
                list(df.columns)
            )

    # -----------------------------------------------------
    # LOGOUT
    # -----------------------------------------------------

    st.markdown("---")

    if st.button(
        "🚪 LOGOUT",
        use_container_width=True
    ):
        st.session_state.logged_in = False
        st.session_state.auth_page = "login"
        st.rerun()
