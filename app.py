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
    layout="wide"
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

    existing_user = cursor.fetchone()

    if existing_user is not None:

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
# PINK + DARK PURPLE DESIGN
# =========================================================

st.markdown(
    """
    <style>

    /* =====================================================
       FULL PAGE BACKGROUND
       ===================================================== */

    .stApp {
        background: #FCE7F3 !important;
    }

    [data-testid="stAppViewContainer"] {
        background: #FCE7F3 !important;
    }

    [data-testid="stMain"] {
        background: #FCE7F3 !important;
    }

    [data-testid="stHeader"] {
        background: #FCE7F3 !important;
    }


    /* =====================================================
       MAIN TEXT
       ===================================================== */

    .stApp,
    .stApp p,
    .stApp span,
    .stApp label {
        color: #24143D;
    }


    /* =====================================================
       MAIN TITLE
       ===================================================== */

    .title {
        font-size: 44px !important;
        font-weight: 800 !important;
        color: #581C87 !important;
    }


    /* =====================================================
       SUBTITLE
       ===================================================== */

    .subtitle {
        font-size: 21px !important;
        font-weight: 500 !important;
        color: #3B234D !important;
    }


    /* =====================================================
       SUBHEADINGS
       ===================================================== */

    h1, h2, h3, h4 {
        color: #581C87 !important;
        font-weight: 800 !important;
    }


    /* =====================================================
       USERNAME / PASSWORD LABELS
       ===================================================== */

    div[data-testid="stTextInput"] label {
        color: #24143D !important;
        font-size: 18px !important;
        font-weight: 800 !important;
    }

    div[data-testid="stTextInput"] label p {
        color: #24143D !important;
        font-size: 18px !important;
        font-weight: 800 !important;
    }


    /* =====================================================
       INPUT BOXES
       ===================================================== */

    div[data-testid="stTextInput"] input {
        background-color: #FFFFFF !important;
        color: #24143D !important;
        font-size: 18px !important;
        font-weight: 600 !important;
        min-height: 48px !important;
        border: 2px solid #C084FC !important;
        border-radius: 12px !important;
    }

    div[data-testid="stTextInput"] input:focus {
        border: 2px solid #7E22CE !important;
        box-shadow: 0 0 0 2px #E9D5FF !important;
    }

    div[data-testid="stTextInput"] input::placeholder {
        color: #6B5B73 !important;
        font-size: 16px !important;
        opacity: 1 !important;
    }


    /* =====================================================
       LOGIN / ACCOUNT / SEGMENTATION BUTTONS
       ===================================================== */

    .stButton > button {
        background-color: #7E22CE !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 12px !important;
        min-height: 54px !important;
        font-size: 18px !important;
        font-weight: 800 !important;
    }

    .stButton > button p {
        color: #FFFFFF !important;
        font-size: 18px !important;
        font-weight: 800 !important;
    }

    .stButton > button:hover {
        background-color: #6B21A8 !important;
        color: #FFFFFF !important;
    }


    /* =====================================================
       TABS
       ===================================================== */

    button[data-baseweb="tab"] {
        color: #581C87 !important;
        font-size: 18px !important;
        font-weight: 800 !important;
    }


    /* =====================================================
       FEATURE CARDS
       ===================================================== */

    .card {
        background: #FFF7FB;
        padding: 24px;
        border-radius: 18px;
        border: 2px solid #F0ABFC;
        margin-bottom: 15px;
        min-height: 150px;
        box-shadow: 0 5px 15px rgba(88, 28, 135, 0.10);
    }

    .card h2 {
        color: #581C87 !important;
        font-size: 24px !important;
    }

    .card p {
        color: #3B234D !important;
        font-size: 17px !important;
    }


    /* =====================================================
       OFFER CARDS
       ===================================================== */

    .offer {
        background: #FFF7FB;
        padding: 22px;
        border-radius: 16px;
        border: 2px solid #F0ABFC;
        margin-bottom: 18px;
        box-shadow: 0 5px 15px rgba(88, 28, 135, 0.10);
    }

    .offer h3 {
        color: #6B21A8 !important;
        font-size: 24px !important;
    }

    .offer p,
    .offer b {
        color: #24143D !important;
        font-size: 17px !important;
    }


    /* =====================================================
       FILE UPLOADER
       ===================================================== */

    section[data-testid="stFileUploaderDropzone"] {
        background: #FFF7FB !important;
        border: 2px dashed #C084FC !important;
        border-radius: 14px !important;
    }


    /* =====================================================
       DATAFRAME
       ===================================================== */

    div[data-testid="stDataFrame"] {
        border: 2px solid #E9D5FF;
        border-radius: 12px;
    }


    /* =====================================================
       DOWNLOAD BUTTON
       ===================================================== */

    .stDownloadButton > button {
        background-color: #7E22CE !important;
        color: #FFFFFF !important;
        border-radius: 12px !important;
        min-height: 54px !important;
        font-size: 18px !important;
        font-weight: 800 !important;
    }

    .stDownloadButton > button p {
        color: #FFFFFF !important;
        font-size: 18px !important;
        font-weight: 800 !important;
    }


    /* =====================================================
       ALERT TEXT
       ===================================================== */

    .stAlert p {
        font-size: 16px !important;
        font-weight: 600 !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# LOGIN / SIGN UP
# =========================================================

if not st.session_state.logged_in:

    st.markdown(
        "<h1 class='title'>🛍️ Smart Customer Segmentation</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p class='subtitle'>"
        "Turn customer data into smart business decisions."
        "</p>",
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

        login_username = st.text_input(
            "👤 Username",
            key="login_user"
        )

        login_password = st.text_input(
            "🔒 Password",
            type="password",
            key="login_pass"
        )

        if st.button(
            "🚀 Login",
            use_container_width=True
        ):

            if (
                login_username.strip() == ""
                or login_password == ""
            ):

                st.warning(
                    "⚠️ Please enter username and password."
                )

            elif login_user(
                login_username.strip(),
                login_password
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
            key="new_user"
        )

        new_email = st.text_input(
            "📧 Email Address",
            key="new_email"
        )

        new_password = st.text_input(
            "🔒 Create Password",
            type="password",
            key="new_pass"
        )

        confirm_password = st.text_input(
            "🔒 Confirm Password",
            type="password",
            key="confirm_pass"
        )

        if st.button(
            "✨ Create Account",
            use_container_width=True
        ):

            username = new_username.strip()
            email = new_email.strip()

            if (
                username == ""
                or email == ""
                or new_password == ""
                or confirm_password == ""
            ):

                st.warning(
                    "⚠️ Please fill all fields."
                )

            elif not valid_email(email):

                st.error(
                    "❌ Please enter a valid email address."
                )

            elif len(new_password) < 4:

                st.warning(
                    "⚠️ Password must contain at least 4 characters."
                )

            elif new_password != confirm_password:

                st.error(
                    "❌ Passwords do not match."
                )

            else:

                account_created = create_account(
                    username,
                    email,
                    new_password
                )

                if account_created:

                    st.success(
                        "🎉 Account created successfully!"
                    )

                    st.info(
                        "Now open the Login tab and login "
                        "with your new account."
                    )

                else:

                    st.error(
                        "❌ Username already exists."
                    )


# =========================================================
# DASHBOARD
# =========================================================

else:

    st.markdown(
        "<h1 class='title'>"
        "📊 Customer Segmentation Dashboard"
        "</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p class='subtitle'>"
        "Welcome to your Smart Customer Segmentation System! 👋"
        "</p>",
        unsafe_allow_html=True
    )

    st.markdown("---")


    # =====================================================
    # FEATURE CARDS
    # =====================================================

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            """
            <div class="card">
            <h2>📁 Upload Dataset</h2>
            <p>Upload your customer CSV data.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            """
            <div class="card">
            <h2>🎯 K-Means Groups</h2>
            <p>Automatically discover customer segments.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:

        st.markdown(
            """
            <div class="card">
            <h2>🤖 Smart Offers</h2>
            <p>Get targeted marketing suggestions.</p>
            </div>
            """,
            unsafe_allow_html=True
        )


    st.markdown("---")


    # =====================================================
    # CSV UPLOAD
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
            .str.replace(
                "\ufeff",
                "",
                regex=False
            )
        )

        df = df.reset_index(drop=True)

        st.success(
            "✅ Dataset uploaded successfully!"
        )


        # =================================================
        # DATA PREVIEW
        # =================================================

        st.subheader("👀 Dataset Preview")

        st.dataframe(
            df,
            use_container_width=True
        )

        st.markdown("---")


        # =================================================
        # FIND COLUMNS
        # =================================================

        income_column = None
        spending_column = None

        for column in df.columns:

            column_name = str(
                column
            ).lower().strip()

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


        # =================================================
        # CHECK COLUMNS
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

                    # =====================================
                    # K-M
