import streamlit as st
import pandas as pd
from sklearn.cluster import KMeans
import sqlite3
import hashlib
import re

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Smart Customer Segmentation",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# DATABASE
# =========================================================

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

    existing = cursor.fetchone()

    if existing:
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


# =========================================================
# SESSION
# =========================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# =========================================================
# CUSTOM DESIGN
# =========================================================

st.markdown(
    """
    <style>

    /* ---------- BACKGROUND ---------- */

    .stApp {
        background:
            radial-gradient(
                circle at top right,
                #ff8fbd 0%,
                transparent 35%
            ),
            linear-gradient(
                135deg,
                #f06a9b 0%,
                #f78fb9 45%,
                #ffd0e1 100%
            );
    }


    /* ---------- MAIN CONTAINER ---------- */

    .block-container {
        max-width: 1150px;
        padding-top: 3rem;
        padding-bottom: 4rem;
    }


    /* ---------- HERO TITLE ---------- */

    .hero {
        text-align: center;
        padding: 25px 10px 20px 10px;
    }

    .hero-small {
        display: inline-block;
        background: #111111;
        color: #ffffff;
        padding: 8px 18px;
        border-radius: 30px;
        font-size: 14px;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 15px;
    }

    .hero-title {
        color: #111111;
        font-size: 52px;
        line-height: 1.05;
        font-weight: 900;
        margin: 5px 0;
    }

    .hero-subtitle {
        color: #24151c;
        font-size: 20px;
        font-weight: 600;
        margin-top: 15px;
    }


    /* ---------- WHITE PANELS ---------- */

    .panel {
        background: rgba(255,255,255,0.96);
        border-radius: 24px;
        padding: 32px;
        margin-top: 20px;
        margin-bottom: 20px;
        border: 1px solid rgba(17,17,17,0.12);
        box-shadow:
            0 18px 45px rgba(50,20,35,0.18);
    }


    /* ---------- LOGIN HEADER ---------- */

    .login-heading {
        text-align: center;
        color: #111111;
        font-size: 30px;
        font-weight: 850;
        margin-bottom: 5px;
    }

    .login-description {
        text-align: center;
        color: #555555;
        font-size: 17px;
        margin-bottom: 20px;
    }


    /* ---------- FEATURE CARDS ---------- */

    .feature-card {
        background: #ffffff;
        border-radius: 20px;
        padding: 25px;
        min-height: 175px;
        border: 1px solid #eeeeee;
        box-shadow:
            0 12px 30px rgba(40,20,30,0.12);
    }

    .feature-icon {
        font-size: 35px;
        margin-bottom: 8px;
    }

    .feature-title {
        color: #111111;
        font-size: 22px;
        font-weight: 800;
    }

    .feature-text {
        color: #555555;
        font-size: 16px;
        line-height: 1.5;
    }


    /* ---------- OFFER CARDS ---------- */

    .offer-card {
        background: #ffffff;
        border-radius: 20px;
        padding: 25px;
        margin: 15px 0;
        border-left: 7px solid #e83e8c;
        box-shadow:
            0 10px 28px rgba(40,20,30,0.12);
    }

    .offer-title {
        color: #111111;
        font-size: 24px;
        font-weight: 850;
        margin-bottom: 8px;
    }

    .offer-text {
        color: #333333;
        font-size: 17px;
        line-height: 1.6;
    }


    /* ---------- BUTTONS ---------- */

    .stButton > button {
        min-height: 55px;
        border-radius: 13px;
        background: #111111;
        color: #ffffff;
        border: 1px solid #111111;
        font-size: 17px;
        font-weight: 750;
        transition: 0.2s;
    }

    .stButton > button:hover {
        background: #e83e8c;
        border-color: #e83e8c;
        color: #ffffff;
    }


    .stDownloadButton > button {
        min-height: 55px;
        border-radius: 13px;
        background: #111111;
        color: #ffffff;
        font-size: 17px;
        font-weight: 750;
    }


    /* ---------- INPUTS ---------- */

    .stTextInput input {
        min-height: 52px;
        border-radius: 12px;
        border: 1px solid #cccccc;
        background: #ffffff;
        color: #111111;
        font-size: 17px;
    }


    /* ---------- TABS ---------- */

    button[data-baseweb="tab"] {
        font-size: 18px !important;
        font-weight: 750 !important;
        color: #333333 !important;
        padding: 15px 25px !important;
    }


    /* ---------- FILE UPLOADER ---------- */

    [data-testid="stFileUploader"] {
        background: #ffffff;
        padding: 20px;
        border-radius: 18px;
        border: 1px solid #dddddd;
    }


    /* ---------- MOBILE ---------- */

    @media (max-width: 768px) {

        .block-container {
            padding: 1.2rem 0.8rem 3rem 0.8rem;
        }

        .hero {
            padding-top: 10px;
        }

        .hero-title {
            font-size: 34px;
        }

        .hero-subtitle {
            font-size: 17px;
        }

        .hero-small {
            font-size: 12px;
            padding: 7px 14px;
        }

        .panel {
            padding: 20px 16px;
            border-radius: 20px;
        }

        .login-heading {
            font-size: 26px;
        }

        .feature-card {
            min-height: auto;
            padding: 20px;
            margin-bottom: 10px;
        }

        .feature-title {
            font-size: 20px;
        }

        .offer-card {
            padding: 20px;
        }

        .offer-title {
            font-size: 21px;
        }

        .offer-text {
            font-size: 16px;
        }

        .stButton > button {
            min-height: 58px;
            font-size: 17px;
        }

        .stDownloadButton > button {
            min-height: 58px;
        }

        .stTextInput input {
            min-height: 55px;
            font-size: 17px;
        }

        button[data-baseweb="tab"] {
            font-size: 16px !important;
            padding: 12px 10px !important;
        }
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# LOGIN / SIGNUP
# =========================================================

if not st.session_state.logged_in:

    st.markdown(
        """
        <div class="hero">

            <div class="hero-small">
                CUSTOMER INTELLIGENCE PLATFORM
            </div>

            <div class="hero-title">
                Smart Customer<br>
                Segmentation
            </div>

            <div class="hero-subtitle">
                Turn customer data into meaningful business insights.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    st.markdown(
        '<div class="panel">',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="login-heading">
            Welcome
        </div>

        <div class="login-description">
            Sign in to analyse customers and discover valuable segments.
        </div>
        """,
        unsafe_allow_html=True
    )


    login_tab, signup_tab = st.tabs(
        [
            "🔐  LOGIN",
            "✨  CREATE ACCOUNT"
        ]
    )


    # LOGIN
    with login_tab:

        st.markdown("<br>", unsafe_allow_html=True)

        username = st.text_input(
            "Username",
            placeholder="Enter your username",
            key="login_username"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
            key="login_password"
        )

        st.markdown("<br>", unsafe_allow_html=True)

        login_clicked = st.button(
            "SIGN IN  →",
            key="login_button",
            use_container_width=True
        )

        if login_clicked:

            if not username.strip():

                st.warning(
                    "Please enter your username."
                )

            elif not password:

                st.warning(
                    "Please enter your password."
                )

            elif login_user(
                username.strip(),
                password
            ):

                st.session_state.logged_in = True

                st.success(
                    "Login successful!"
                )

                st.rerun()

            else:

                st.error(
                    "Invalid username or password."
                )


    # CREATE ACCOUNT
    with signup_tab:

        st.markdown("<br>", unsafe_allow_html=True)

        new_username = st.text_input(
            "Username",
            placeholder="Choose a username",
            key="signup_username"
        )

        new_email = st.text_input(
            "Email",
            placeholder="Enter your email address",
            key="signup_email"
        )

        new_password = st.text_input(
            "Password",
            type="password",
            placeholder="Create a password",
            key="signup_password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            placeholder="Confirm your password",
            key="signup_confirm"
        )

        st.markdown("<br>", unsafe_allow_html=True)

        signup_clicked = st.button(
            "CREATE ACCOUNT  →",
            key="signup_button",
            use_container_width=True
        )

        if signup_clicked:

            username = new_username.strip()
            email = new_email.strip()

            if not username:

                st.warning(
                    "Please enter a username."
                )

            elif not email:

                st.warning(
                    "Please enter an email address."
                )

            elif not valid_email(email):

                st.error(
                    "Please enter a valid email address."
                )

            elif not new_password:

                st.warning(
                    "Please create a password."
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
                    username,
                    email,
                    new_password
                )

                if created:

                    st.success(
                        "Account created successfully!"
                    )

                    st.info(
                        "Now open LOGIN and sign in."
                    )

                else:

                    st.error(
                        "Username already exists."
                    )


    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# =========================================================
# DASHBOARD
# =========================================================

if st.session_state.logged_in:

    st.markdown(
        """
        <div class="hero">

            <div class="hero-small">
                CUSTOMER ANALYTICS
            </div>

            <div class="hero-title">
                Smart Customer<br>
                Segmentation
            </div>

            <div class="hero-subtitle">
                Understand your customers. Discover your segments.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # FEATURE CARDS

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">📁</div>
                <div class="feature-title">
                    Upload Data
                </div>
                <div class="feature-text">
                    Upload your customer CSV
                    and start analysing your data.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    with col2:

        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">🎯</div>
                <div class="feature-title">
                    Customer Groups
                </div>
                <div class="feature-text">
                    K-Means automatically discovers
                    four customer segments.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    with col3:

        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">💡</div>
                <div class="feature-title">
                    Smart Insights
                </div>
                <div class="feature-text">
                    Get useful marketing ideas
                    for each customer group.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    st.markdown("<br>", unsafe_allow_html=True)


    # UPLOAD

    st.markdown(
        """
        <div class="panel">
        <h2>📂 Upload Customer Dataset</h2>
        <p>
        Upload a CSV containing customer information.
        </p>
        </div>
        """,
        unsafe_allow_html=True
    )


    uploaded_file = st.file_uploader(
        "Choose CSV file",
        type=["csv"]
    )


    if uploaded_file is None:

        st.info(
            "Upload your CSV file above to begin."
        )


    if uploaded_file is not None:

        try:

            df = pd.read_csv(
                uploaded_file
            )

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
                "Unable to read the CSV file."
            )

            st.write(str(error))

            st.stop()


        st.success(
            "Dataset uploaded successfully!"
        )


        st.subheader(
            "👀 Dataset Preview"
        )

        st.dataframe(
            df,
            use_container_width=True
        )


        # FIND COLUMNS

        income_column = None
        spending_column = None

        for column in df.columns:

            name = (
                str(column)
                .lower()
                .strip()
            )

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


        if (
            income_column is None
            or spending_column is None
        ):

            st.error(
                "Annual Income or Spending Score "
                "column was not found."
            )

            st.write(
                "Columns found:"
            )

            st.write(
                list(df.columns)
            )


        if (
            income_column is not None
            and spending_column is not None
        ):

            st.markdown("---")

            st.subheader(
                "🎯 Customer Segmentation"
            )

            run_button = st.button(
                "RUN CUSTOMER SEGMENTATION  →",
                use_container_width=True,
                key="run_button"
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
                        "At least 4 valid customers are required."
                    )


                else:

                    model = KMeans(
                        n_clusters=4,
                        random_state=42,
                        n_init=10
                    )

                    cluster_numbers = (
                        model.fit_predict(
                            valid_data
                        )
                    )


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
                        "Customer segmentation completed successfully!"
                    )


                    # GROUP TABLE

                    st.subheader(
                        "👥 Customer Groups"
                    )

                    st.dataframe(
                        df,
                        use_container_width=True
                    )


                    # SUMMARY

                    centers = (
                        model.cluster_centers_
                    )

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


                    # GROUP IDENTIFICATION

                    vip_group = None
                    potential_group = None
                    deal_group = None
                    growth_group = None


                    for cluster in range(4):

                        income = (
                            centers[cluster][0]
                        )

                        spending = (
                            centers[cluster][1]
                        )

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


                    # INSIGHTS

                    st.markdown("---")

                    st.subheader(
                        "💡 Smart Customer Insights"
                    )


                    if vip_group is not None:

                        st.markdown(
                            """
                            <div class="offer-card">

                                <div class="offer-title">
                                    💎 VIP Champions
                                </div>

                                <div class="offer-text">
                                    <b>Customer type:</b>
                                    High income + high spending.
                                    <br><br>

                                    <b>Recommended offer:</b>
                                    Premium products, loyalty rewards
                                    and exclusive early access.
                                    <br><br>

                                    <b>Marketing strategy:</b>
                                    Build long-term loyalty.
                                </div>

                            </div>
                            """,
                            unsafe_allow_html=True
                        )


                    if potential_group is not None:

                        st.markdown(
                            """
                            <div class="offer-card">

                                <div class="offer-title">
                                    🌟 Hidden Potential
                                </div>

                                <div class="offer-text">
                                    <b>Customer type:</b>
                                    High income + lower spending.
                                    <br><br>

                                    <b>Recommended offer:</b>
                                    Personalised discounts,
                                    recommendations and trial offers.
                                    <br><br>

                                    <b>Marketing strategy:</b>
                                    Encourage more frequent purchases.
                                </div>

                            </div>
                            """,
                            unsafe_allow_html=True
                        )


                    if deal_group is not None:

                        st.markdown(
                            """
                            <div class="offer-card">

                                <div class="offer-title">
                                    🔥 Deal Lovers
                                </div>

                                <div class="offer-text">
                                    <b>Customer type:</b>
                                    Lower income + high spending.
                                    <br><br>

                                    <b>Recommended offer:</b>
                                    Bundle deals, value packs
                                    and limited-time offers.
                                    <br><br>

                                    <b>Marketing strategy:</b>
                                    Reward customer engagement.
                                </div>

                            </div>
                            """,
                            unsafe_allow_html=True
                        )


                    if growth_group is not None:

                        st.markdown(
                            """
                            <div class="offer-card">

                                <div class="offer-title">
                                    🌱 Growth Customers
                                </div>

                                <div class="offer-text">
                                    <b>Customer type:</b>
                                    Lower income + lower spending.
                                    <br><br>

                                    <b>Recommended offer:</b>
                                    Welcome offers, affordable bundles
                                    and first-purchase incentives.
                                    <br><br>

                                    <b>Marketing strategy:</b>
                                    Encourage first and repeat purchases.
                                </div>

                            </div>
                            """,
                            unsafe_allow_html=True
                        )


                    # DOWNLOAD

                    st.markdown("---")

                    st.subheader(
                        "📥 Download Report"
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
                        "DOWNLOAD CSV REPORT  ↓",
                        data=csv_data,
                        file_name="customer_segments.csv",
                        mime="text/csv",
                        use_container_width=True
                    )


    # LOGOUT

    st.markdown("---")

    if st.button(
        "🚪 LOG OUT",
        use_container_width=True
    ):

        st.session_state.logged_in = False
        st.rerun()
