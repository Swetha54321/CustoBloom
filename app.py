import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="CustoBloom",
    page_icon="🌺",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at 10% 10%, rgba(168,85,247,.18), transparent 28%),
                radial-gradient(circle at 90% 15%, rgba(236,72,153,.14), transparent 30%),
                linear-gradient(135deg, #070817, #15112b 55%, #080b1d);
    color: #f8fafc;
}

html, body, [class*="css"] {
    font-family: "Trebuchet MS", Arial, sans-serif;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0b0c1d, #17122f, #090a18);
    border-right: 1px solid rgba(255,255,255,.08);
}

.brand {
    text-align: center;
    padding: 18px 5px 22px;
}

.logo {
    width: 78px;
    height: 78px;
    margin: auto;
    border-radius: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 44px;
    background: linear-gradient(135deg, rgba(236,72,153,.28), rgba(139,92,246,.30));
    box-shadow: 0 0 35px rgba(168,85,247,.28);
    border: 1px solid rgba(255,255,255,.12);
}

.brand-name, .main-title {
    background: linear-gradient(90deg, #f9a8d4, #c084fc, #818cf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 900;
}

.brand-name {
    font-family: Georgia, serif;
    font-size: 27px;
    margin-top: 10px;
}

.main-title {
    font-family: Georgia, serif;
    font-size: 46px;
    letter-spacing: 1px;
}

.subtitle {
    color: #9da8bc;
    font-size: 16px;
    margin-bottom: 24px;
}

.welcome, .card, .insight {
    background: linear-gradient(145deg, rgba(30,27,65,.88), rgba(14,15,35,.92));
    border: 1px solid rgba(255,255,255,.08);
    border-radius: 22px;
    box-shadow: 0 12px 35px rgba(0,0,0,.28);
}

.welcome {
    padding: 24px;
    margin-bottom: 24px;
}

.card {
    padding: 20px;
    min-height: 145px;
    transition: .25s;
}

.card:hover {
    transform: translateY(-5px);
    border-color: rgba(192,132,252,.4);
}

.icon {
    font-size: 32px;
}

.number {
    color: #fff;
    font-size: 29px;
    font-weight: 800;
}

.label {
    color: #9da8bc;
    font-size: 14px;
}

.segment {
    padding: 22px;
    min-height: 190px;
    border-radius: 22px;
    background: linear-gradient(145deg, rgba(29,25,62,.92), rgba(14,15,35,.90));
    border: 1px solid rgba(255,255,255,.08);
    transition: .25s;
}

.segment:hover {
    transform: translateY(-6px);
    border-color: rgba(236,72,153,.4);
}

.segment h3 {
    color: #fff;
    margin: 8px 0;
}

.segment p, .welcome p, .insight p {
    color: #aeb8ca;
    line-height: 1.55;
}

.insight {
    padding: 20px;
    margin: 12px 0;
    border-left: 4px solid #c084fc;
}

.insight h3 {
    color: #e9d5ff;
}

.footer {
    text-align: center;
    color: #69758a;
    padding: 30px 5px 10px;
    font-size: 13px;
}

.stButton > button {
    width: 100%;
    border: 0;
    border-radius: 13px;
    padding: 11px 18px;
    background: linear-gradient(90deg, #a855f7, #ec4899);
    color: white;
    font-weight: 700;
}

.stTextInput input {
    background: #0d0f24 !important;
    color: white !important;
    border: 1px solid rgba(255,255,255,.12) !important;
    border-radius: 12px !important;
}
</style>
""", unsafe_allow_html=True)


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


if not st.session_state.logged_in:

    st.markdown("""
    <div style="text-align:center; padding-top:70px;">
        <div class="logo">🌺</div>
        <div class="main-title">CustoBloom</div>
        <div class="subtitle">Smart Customer Segmentation for Smarter Marketing</div>
    </div>
    """, unsafe_allow_html=True)

    username = st.text_input("👤 Username")
    password = st.text_input("🔐 Password", type="password")

    if st.button("✨ Enter CustoBloom"):

        if username == "admin" and password == "admin123":
            st.session_state.logged_in = True
            st.rerun()

        else:
            st.error("Invalid username or password.")

    st.markdown(
        '<div class="footer">Demo Login: admin / admin123</div>',
        unsafe_allow_html=True
    )

    st.stop()


with st.sidebar:

    st.markdown("""
    <div class="brand">
        <div class="logo">🌺</div>
        <div class="brand-name">CustoBloom</div>
        <div style="color:#7f8aa3;font-size:11px;">SMART MARKETING AI</div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "MENU",
        [
            "🏠 Dashboard",
            "👥 Customers",
            "🎯 Segmentation",
            "📊 Analytics",
            "🤖 Smart Insights",
            "ℹ️ About"
        ]
    )

    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.rerun()


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
    <div class="welcome">
        <h2 style="color:white;">👋 Welcome back, Admin</h2>
        <p>
            Discover customer patterns, understand spending behaviour,
            and create smarter marketing strategies using AI-powered segmentation.
        </p>
    </div>
    """, unsafe_allow_html=True)


    cols = st.columns(4)

    metrics = [
        ("👥", "200", "Total Customers"),
        ("🎯", "4", "Customer Segments"),
        ("🧠", "K-Means", "ML Algorithm"),
        ("📈", "94%", "Insight Score")
    ]

    for col, (icon, number, label) in zip(cols, metrics):

        with col:

            st.markdown(
                f'''
                <div class="card">
                    <div class="icon">{icon}</div>
                    <div class="number">{number}</div>
                    <div class="label">{label}</div>
                </div>
                ''',
                unsafe_allow_html=True
            )


    st.markdown("<br>", unsafe_allow_html=True)

    st.subheader("🌸 Customer Segments")

    cols = st.columns(4)

    segments = [
        (
            "💎",
            "Premium Customers",
            "High income and high spending. Ideal for premium products and exclusive offers."
        ),
        (
            "🛍️",
            "Regular Customers",
            "Stable purchasing behaviour. Suitable for loyalty campaigns and regular promotions."
        ),
        (
            "💰",
            "High Income",
            "High earning customers with lower spending. A strong opportunity for targeted offers."
        ),
        (
            "❤️",
            "Loyal Customers",
            "Consistent customers who are ideal for rewards and retention strategies."
        )
    ]

    for col, (icon, title, text) in zip(cols, segments):

        with col:

            st.markdown(
                f'''
                <div class="segment">
                    <div class="icon">{icon}</div>
                    <h3>{title}</h3>
                    <p>{text}</p>
                </div>
                ''',
                unsafe_allow_html=True
            )


    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="insight">
        <h3>💡 Smart Marketing Opportunity</h3>
        <p>
            Use personalised recommendations, exclusive offers and loyalty
            rewards to improve customer engagement and retention.
        </p>
    </div>
    """, unsafe_allow_html=True)


elif page == "👥 Customers":

    st.markdown(
        '<div class="main-title">Customer Explorer</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Explore customer information and behaviour</div>',
        unsafe_allow_html=True
    )

    df = pd.DataFrame({
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
            39, 81, 65, 55, 72, 45, 30, 20
        ]
    })

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )


elif page == "🎯 Segmentation":

    st.markdown(
        '<div class="main-title">AI Segmentation</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Customer groups powered by K-Means clustering</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="welcome">
        <h2 style="color:white;">🧠 How it works</h2>
        <p>
            K-Means groups customers with similar characteristics,
            such as annual income and spending score, into meaningful segments.
        </p>
    </div>
    """, unsafe_allow_html=True)

    df = pd.DataFrame({
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
        df,
        use_container_width=True,
        hide_index=True
    )


elif page == "📊 Analytics":

    st.markdown(
        '<div class="main-title">Analytics</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Visual understanding of customer segments</div>',
        unsafe_allow_html=True
    )

    chart = pd.DataFrame(
        {"Customers": [48, 62, 35, 55]},
        index=["Premium", "Regular", "High Income", "Loyal"]
    )

    st.bar_chart(chart)

    st.subheader("💰 Spending Behaviour")

    spending = pd.DataFrame(
        {"Spending Score": [82, 58, 25, 74]},
        index=["Premium", "Regular", "High Income", "Loyal"]
    )

    st.line_chart(spending)


elif page == "🤖 Smart Insights":

    st.markdown(
        '<div class="main-title">Smart Insights</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Actionable recommendations for smarter marketing</div>',
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
            "Send the right offer to the right customer using segmentation."
        )
    ]

    for title, text in insights:

        st.markdown(
            f'''
            <div class="insight">
                <h3>{title}</h3>
                <p>{text}</p>
            </div>
            ''',
            unsafe_allow_html=True
        )


elif page == "ℹ️ About":

    st.markdown(
        '<div class="main-title">
