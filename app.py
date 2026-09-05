import streamlit as st
import pandas as pd
import numpy as np

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="CustoBloom | Smart Customer Segmentation",
    page_icon="🌺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>

/* ---------- MAIN BACKGROUND ---------- */
.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(168, 85, 247, 0.18), transparent 30%),
        radial-gradient(circle at 90% 20%, rgba(236, 72, 153, 0.15), transparent 30%),
        linear-gradient(135deg, #070817 0%, #11132b 50%, #090b20 100%);
    color: #f8fafc;
}

/* ---------- GLOBAL TEXT ---------- */
html, body, [class*="css"] {
    font-family: "Trebuchet MS", Arial, sans-serif;
}

p, label, span {
    color: #dbe4f0;
}

/* ---------- SIDEBAR ---------- */
section[data-testid="stSidebar"] {
    background:
        linear-gradient(180deg, #0c0d20 0%, #14112d 55%, #0a0b1b 100%);
    border-right: 1px solid rgba(255,255,255,0.08);
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #ffffff;
}

/* ---------- BRAND ---------- */
.brand-box {
    text-align: center;
    padding: 15px 5px 25px 5px;
}

.brand-flower {
    width: 75px;
    height: 75px;
    margin: auto;
    border-radius: 25px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 43px;

    background: linear-gradient(
        135deg,
        rgba(236,72,153,0.30),
        rgba(139,92,246,0.35)
    );

    border: 1px solid rgba(255,255,255,0.14);
    box-shadow:
        0 0 30px rgba(168,85,247,0.35),
        inset 0 0 20px rgba(255,255,255,0.04);
}

.brand-name {
    margin-top: 12px;
    font-size: 26px;
    font-weight: 800;
    background: linear-gradient(
        90deg,
        #f9a8d4,
        #c084fc,
        #818cf8
    );
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* ---------- MAIN TITLE ---------- */
.main-title {
    font-family: Georgia, "Times New Roman", serif;
    font-size: 45px;
    font-weight: 900;
    letter-spacing: 1px;

    background: linear-gradient(
        90deg,
        #f9a8d4,
        #d8b4fe,
        #a5b4fc,
        #f9a8d4
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    margin-bottom: 4px;
}

.subtitle {
    color: #aab4c8;
    font-size: 16px;
    margin-bottom: 25px;
}

/* ---------- WELCOME BOX ---------- */
.welcome-box {
    padding: 25px;
    border-radius: 22px;

    background:
        linear-gradient(
            135deg,
            rgba(168,85,247,0.14),
            rgba(236,72,153,0.08)
        );

    border: 1px solid rgba(192,132,252,0.20);

    box-shadow:
        0 10px 40px rgba(0,0,0,0.25);

    margin-bottom: 25px;
}

.welcome-title {
    font-size: 25px;
    font-weight: 700;
    color: #ffffff;
}

.welcome-text {
    color: #b9c3d4;
    font-size: 15px;
}

/* ---------- METRIC CARDS ---------- */
.metric-card {
    padding: 22px;
    border-radius: 20px;

    background:
        linear-gradient(
            145deg,
            rgba(30,27,65,0.85),
            rgba(18,18,42,0.85)
        );

    border: 1px solid rgba(255,255,255,0.08);

    box-shadow:
        0 12px 35px rgba(0,0,0,0.30);

    transition: 0.3s ease;
}

.metric-card:hover {
    transform: translateY(-6px);
    border-color: rgba(192,132,252,0.45);
    box-shadow:
        0 15px 45px rgba(139,92,246,0.18);
}

.metric-icon {
    font-size: 30px;
}

.metric-number {
    font-size: 30px;
    font-weight: 800;
    color: #ffffff;
    margin-top: 5px;
}

.metric-label {
    color: #9ca9bd;
    font-size: 14px;
}

/* ---------- SEGMENT CARDS ---------- */
.segment-card {
    min-height: 185px;
    padding: 22px;
    border-radius: 22px;

    background:
        linear-gradient(
            145deg,
            rgba(29,25,62,0.92),
            rgba(14,15,35,0.90)
        );

    border: 1px solid rgba(255,255,255,0.08);

    box-shadow: 0 12px 35px rgba(0,0,0,0.25);

    transition: 0.3s ease;
}

.segment-card:hover {
    transform: translateY(-7px) scale(1.01);
    border-color: rgba(236,72,153,0.40);
}

.segment-icon {
    font-size: 38px;
}

.segment-title {
    font-size: 19px;
    font-weight: 800;
    color: #ffffff;
    margin-top: 10px;
}

.segment-description {
    color: #aeb8ca;
    font-size: 14px;
    line-height: 1.5;
}

/* ---------- INSIGHT BOX ---------- */
.insight {
    padding: 20px;
    border-radius: 18px;

    background:
        linear-gradient(
            135deg,
            rgba(99,102,241,0.12),
            rgba(168,85,247,0.10)
        );

    border-left: 4px solid #c084fc;

    margin-bottom: 15px;
}

.insight-title {
    color: #e9d5ff;
    font-size: 17px;
    font-weight: 700;
}

.insight-text {
    color: #b7c2d4;
    font-size: 14px;
}

/* ---------- LOGIN ---------- */
.login-wrapper {
    max-width: 480px;
    margin: 70px auto;
    padding: 40px;

    background:
        linear-gradient(
            145deg,
            rgba(26,23,55,0.95),
            rgba(12,14,32,0.96)
        );

    border: 1px solid rgba(192,132,252,0.18);

    border-radius: 28px;

    box-shadow:
        0 20px 70px rgba(0,0,0,0.45),
        0 0 40px rgba(139,92,246,0.08);

    text-align: center;
}

.login-flower {
    font-size: 65px;
    margin-bottom: 5px;
}

.login-title {
    font-family: Georgia, serif;
    font-size: 40px;
    font-weight: 900;

    background: linear-gradient(
        90deg,
        #f9a8d4,
        #c084fc,
        #818cf8
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.login-subtitle {
    color: #9da8bc;
    margin-bottom: 25px;
}

/* ---------- INPUTS ---------- */
.stTextInput input,
.stSelectbox div,
.stNumberInput input {
    background-color: rgba(10,12,28,0.85) !important;
    color: #ffffff !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 12px !important;
}

/* ---------- BUTTON ---------- */
.stButton > button {
    width: 100%;
    border: none;

    border-radius: 14px;

    background:
        linear-gradient(
            90deg,
            #a855f7,
            #ec4899
        );

    color: white;
    font-weight: 700;

    padding: 12px 20px;

    box-shadow:
        0 8px 25px rgba(168,85,247,0.25);

    transition: 0.3s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow:
        0 12px 35px rgba(236,72,153,0.30);
}

/* ---------- DATAFRAME ---------- */
div[data-testid="stDataFrame"] {
    border-radius: 15px;
    overflow: hidden;
}

/* ---------- FOOTER ---------- */
.footer {
    text-align: center;
    padding: 30px 10px 10px 10px;
    color: #69758a;
    font-size: 13px;
}

.footer strong {
    color: #c084fc;
}

/* ---------- DIVIDER ---------- */
hr {
    border-color: rgba(255,255,255,0.08) !important;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# LOGIN SYSTEM
# =========================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


if not st.session_state.logged_in:

    st.markdown("""
    <div class="login-wrapper">

        <div class="login-flower">🌺</div>

        <div class="login-title">
            CustoBloom
        </div>

        <div class="login-subtitle">
            Smart Customer Segmentation
        </div>

    </div>
    """, unsafe_allow_html=True)

    username = st.text_input("👤 Username")
    password = st.text_input("🔐 Password", type="password")

    if st.button("✨ Enter Dashboard"):

        if username == "admin" and password == "admin123":
            st.session_state.logged_in = True
            st.success("Welcome to CustoBloom! 🌺")
            st.rerun()

        else:
            st.error("Invalid username or password.")

    st.markdown("""
    <div class="footer">
        Demo Login • Username: <strong>admin</strong> • Password: <strong>admin123</strong>
    </div>
    """, unsafe_allow_html=True)

    st.stop()


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("""
    <div class="brand-box">

        <div class="brand-flower">
            🌺
        </div>

        <div class="brand-name">
            CustoBloom
        </div>

        <div style="color:#7f8aa3;font-size:12px;">
            SMART MARKETING AI
        </div>

    </div>
    """, unsafe_allow_html=True)

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "👥 Customers",
            "🎯 Segmentation",
            "📊 Analytics",
            "🤖 Smart Insights",
            "ℹ️ About"
        ]
    )

    st.divider()

    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.rerun()


# =========================================================
# DASHBOARD
# =========================================================

if page == "🏠 Dashboard":

    st.markdown(
        '<div class="main-title">CustoBloom</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Smart Customer Segmentation for Smarter Marketing</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="welcome-box">

        <div class="welcome-title">
            👋 Welcome back, Admin
        </div>

        <div class="welcome-text">
            Discover customer patterns, understand spending behaviour,
            and create smarter marketing strategies using AI-powered segmentation.
        </div>

    </div>
    """, unsafe_allow_html=True)

    # Metrics
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-icon">👥</div>
            <div class="metric-number">200</div>
            <div class="metric-label">Total Customers</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-icon">🎯</div>
            <div class="metric-number">4</div>
            <div class="metric-label">Customer Segments</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-icon">🧠</div>
            <div class="metric-number">K-Means</div>
            <div class="metric-label">ML Algorithm</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-icon">📈</div>
            <div class="metric-number">94%</div>
            <div class="metric-label">Model Insight Score</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.subheader("🌸 Customer Segments")

    s1, s2, s3, s4 = st.columns(4)

    with s1:
        st.markdown("""
        <div class="segment-card">
            <div class="segment-icon">💎</div>
            <div class="segment-title">Premium Customers</div>
            <div class="segment-description">
                High income and high spending behaviour.
                Ideal for premium products and exclusive offers.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with s2:
        st.markdown("""
        <div class="segment-card">
            <div class="segment-icon">🛍️</div>
            <div class="segment-title">Regular Customers</div>
            <div class="segment-description">
                Stable purchasing behaviour.
                Suitable for loyalty campaigns and regular promotions.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with s3:
        st.markdown("""
        <div class="segment-card">
            <div class="segment-icon">💰</div>
            <div class="segment-title">High Income</div>
            <div class="segment-description">
                High earning customers with relatively low spending.
                Opportunity for targeted conversion campaigns.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with s4:
        st.markdown("""
        <div class="segment-card">
            <div class="segment-icon">❤️</div>
            <div class="segment-title">Loyal Customers</div>
            <div class="segment-description">
                Consistent customers with strong engagement.
                Best suited for rewards and retention strategies.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.subheader("✨ Quick AI Insight")

    st.markdown("""
    <div class="insight">

        <div class="insight-title">
            💡 Marketing Opportunity
        </div>

        <div class="insight-text">
            Premium customers can be targeted with exclusive products,
            personalised recommendations and loyalty rewards to increase
            customer lifetime value.
        </div>

    </div>
    """, unsafe_allow_html=True)


# =========================================================
# CUSTOMERS
# =========================================================

elif page == "👥 Customers":

    st.markdown(
        '<div class="main-title">Customer Explorer</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Explore customer information and behaviour</div>',
        unsafe_allow_html=True
    )

    customer_data = {
        "Customer ID": [1, 2, 3, 4, 5, 6, 7, 8],
        "Gender": [
            "Male", "Female", "Female", "Male",
            "Female", "Male", "Female", "Male"
        ],
        "Age": [19, 21, 25, 31, 35, 40, 45, 50],
        "Annual Income": [
            15000, 18000, 25000, 45000,
            55000, 65000, 80000, 100000
        ],
        "Spending Score": [
            39, 81, 65, 55,
            72, 45, 30, 20
        ]
    }

    df = pd.DataFrame(customer_data)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    a, b, c = st.columns(3)

    with a:
        st.metric("Average Age", "33.3")

    with b:
        st.metric("Average Income", "₹49.8K")

    with c:
        st.metric("Average Spending", "50.9")


# =========================================================
# SEGMENTATION
# =========================================================

elif page == "🎯 Segmentation":

    st.markdown(
        '<div class="main-title">AI Segmentation</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Grouping customers using machine learning</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="welcome-box">

        <div class="welcome-title">
            🧠 K-Means Clustering
        </div>

        <div class="welcome-text">
            CustoBloom uses customer characteristics such as
            annual income and spending score to identify meaningful
            customer groups.
        </div>

    </div>
    """, unsafe_allow_html=True)

    st.subheader("🎯 Identified Segments")

    segments = pd.DataFrame({
        "Segment": [
            "Premium Customers",
            "Regular Customers",
            "High Income - Low Spenders",
            "Loyal Customers"
        ],
        "Customer Count": [48, 62, 35, 55],
        "Marketing Priority": [
            "Very High",
            "Medium",
            "High",
            "Very High"
        ]
    })

    st.dataframe(
        segments,
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# ANALYTICS
# =========================================================

elif page == "📊 Analytics":

    st.markdown(
        '<div class="main-title">Analytics</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Visual understanding of customer segments</div>',
        unsafe_allow_html=True
    )

    chart_data = pd.DataFrame({
        "Customers": [48, 62, 35, 55]
    }, index=[
        "Premium",
        "Regular",
        "High Income",
        "Loyal"
    ])

    st.subheader("📈 Customers by Segment")

    st.bar_chart(chart_data)

    st.markdown("<br>", unsafe_allow_html=True)

    st.subheader("💰 Spending Behaviour")

    spending = pd.DataFrame({
        "Spending Score": [82, 58, 25, 74]
    }, index=[
        "Premium",
        "Regular",
        "High Income",
        "Loyal"
    ])

    st.line_chart(spending)


# =========================================================
# SMART INSIGHTS
# =========================================================

elif page == "🤖 Smart Insights":

    st.markdown(
        '<div class="main-title">Smart Insights</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">AI-inspired recommendations for smarter marketing</div>',
        unsafe_allow_html=True
    )

    insights = [
        (
            "💎 Premium Customers",
            "Offer exclusive products, VIP rewards and personalised recommendations."
        ),
        (
            "🛍️ Regular Customers",
            "Use loyalty points, seasonal discounts and personalised campaigns."
        ),
        (
            "💰 High Income Customers",
            "Introduce premium products and personalised offers to increase spending."
        ),
        (
            "❤️ Loyal Customers",
            "Focus on retention through rewards, appreciation campaigns and early access."
        ),
        (
            "📢 Overall Strategy",
            "Use customer segmentation to send the right offer to the right customer."
        )
    ]

    for title, text in insights:

        st.markdown(f"""
        <div class="insight">

            <div class="insight-title">
                {title}
            </div>

            <div class="insight-text">
                {text}
            </div>

        </div>
        """, unsafe_allow_html=True)


# =========================================================
# ABOUT
# =========================================================

elif page == "ℹ️ About":

    st.markdown(
        '<div class="main-title">About CustoBloom</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Smart Customer Segmentation for Smarter Marketing</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="welcome-box">

        <div class="welcome-title">
            🌺 What is CustoBloom?
        </div>

        <div class="welcome-text">
            CustoBloom is a smart customer segmentation platform designed
            to help businesses understand their customers and improve
            marketing decisions using machine learning.
            <br><br>
            The system analyses customer characteristics and groups
            customers into meaningful segments using the K-Means algorithm.
        </div>

    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="segment-card">

            <div class="segment-icon">🎯</div>

            <div class="segment-title">
                Project Goal
            </div>

            <div class="segment-description">
                Transform customer data into useful marketing insights
                and help businesses create personalised strategies.
            </div>

        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="segment-card">

            <div class="segment-icon">🤖</div>

            <div class=
