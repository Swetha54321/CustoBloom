import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import hashlib
import re
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Smart Customer Segmentation",
    page_icon="📊",
    layout="wide"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 48px;
        font-weight: 800;
        text-align: center;
        margin-top: 30px;
        margin-bottom: 10px;
    }

    .subtitle {
        font-size: 20px;
        text-align: center;
        color: #666666;
        margin-bottom: 35px;
    }

    .hero-box {
        padding: 45px;
        border-radius: 20px;
        text-align: center;
        background: linear-gradient(135deg, #eef2ff, #f8fafc);
        margin-bottom: 30px;
    }

    .feature-box {
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #dddddd;
        min-height: 180px;
        margin-bottom: 20px;
    }

    .feature-title {
        font-size: 22px;
        font-weight: 700;
    }

    .feature-text {
        color: #666666;
        font-size: 16px;
    }

    .section-title {
        font-size: 30px;
        font-weight: 700;
        margin-top: 25px;
        margin-bottom: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True
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


# =========================================================
# PASSWORD HASHING
# =========================================================

def hash_password(password):

    return hashlib.sha256(
        password.encode()
    ).hexdigest()


# =========================================================
# EMAIL VALIDATION
# =========================================================

def valid_email(email):

    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    return re.match(pattern, email) is not None


# =========================================================
# CREATE ACCOUNT
# =========================================================

def create_account(username, email, password):

    conn = get_database()

    cursor = conn.cursor()

    cursor.execute(
        "SELECT username FROM users WHERE username = ?",
        (username,)
    )

    existing_user = cursor.fetchone()

    if existing_user:

        conn.close()

        return False, "Username already exists."

    cursor.execute(
        "SELECT email FROM users WHERE email = ?",
        (email,)
    )

    existing_email = cursor.fetchone()

    if existing_email:

        conn.close()

        return False, "Email already exists."

    cursor.execute(
        "INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
        (
            username,
            hash_password(password),
            email
        )
    )

    conn.commit()

    conn.close()

    return True, "Account created successfully."


# =========================================================
# LOGIN
# =========================================================

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


# =========================================================
# SESSION STATE
# =========================================================

if "logged_in" not in st.session_state:

    st.session_state.logged_in = False


if "username" not in st.session_state:

    st.session_state.username = ""


if "page" not in st.session_state:

    st.session_state.page = "home"


# =========================================================
# LOGOUT
# =========================================================

def logout():

    st.session_state.logged_in = False

    st.session_state.username = ""

    st.session_state.page = "home"

    st.rerun()


# =========================================================
# HOME PAGE
# =========================================================

def home_page():

    st.markdown(
        '<div class="hero-box">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="main-title">📊 Smart Customer Segmentation</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Understand your customers. Discover valuable segments. '
        'Make smarter business decisions.'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <p style="font-size:18px;text-align:center;">
        An intelligent Machine Learning based customer segmentation
        system using K-Means clustering.
        </p>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:

        if st.button(
            "🔐 Login",
            use_container_width=True
        ):

            st.session_state.page = "auth"

            st.rerun()

    with col2:

        if st.button(
            "🚀 Get Started",
            use_container_width=True
        ):

            st.session_state.page = "auth"

            st.rerun()

    with col3:

        if st.button(
            "📖 Learn More",
            use_container_width=True
        ):

            st.session_state.page = "learn"

            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title">✨ What Our System Can Do</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            """
            <div class="feature-box">
                <div class="feature-title">📁 Upload Dataset</div>
                <br>
                <div class="feature-text">
                Upload your customer CSV dataset and preview
                the information instantly.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            """
            <div class="feature-box">
                <div class="feature-title">🤖 Machine Learning</div>
                <br>
                <div class="feature-text">
                K-Means clustering automatically groups customers
                according to their behaviour.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:

        st.markdown(
            """
            <div class="feature-box">
                <div class="feature-title">💡 Smart Insights</div>
                <br>
                <div class="feature-text">
                Get useful customer insights and targeted offer
                suggestions for each segment.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")

    st.info(
        "💡 Login to access the Customer Segmentation Dashboard."
    )


# =========================================================
# LE
