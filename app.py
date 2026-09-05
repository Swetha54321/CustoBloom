import streamlit as st

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="CustoBloom",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #fff5fb 0%, #f5f0ff 50%, #eef7ff 100%);
}

/* Main title */
.main-title {
    font-size: 48px;
    font-weight: 800;
    background: linear-gradient(90deg, #d946ef, #7c3aed, #2563eb);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0;
}

.subtitle {
    color: #64748b;
    font-size: 17px;
    margin-top: -5px;
}

/* Welcome box */
.welcome-box {
    padding: 28px;
    border-radius: 24px;
    background: linear-gradient(120deg, #fce7f3, #ede9fe, #dbeafe);
    margin: 20px 0 30px 0;
    box-shadow: 0 10px 30px rgba(124, 58, 237, 0.10);
}

.welcome-title {
    font-size: 30px;
    font-weight: 700;
    color: #312e81;
}

.welcome-text {
    color: #475569;
    font-size: 16px;
}

/* Metric cards */
.metric-card {
    padding: 24px;
    border-radius: 20px;
    background: rgba(255,255,255,0.85);
    border: 1px solid rgba(255,255,255,0.9);
    box-shadow: 0 8px 25px rgba(15,23,42,0.08);
    text-align: center;
    margin-bottom: 20px;
}

.metric-icon {
    font-size: 32px;
}

.metric-number {
    font-size: 30px;
    font-weight: 800;
    color: #4c1d95;
}

.metric-label {
    color: #64748b;
    font-size: 14px;
}

/* Segment cards */
.segment-card {
    padding: 22px;
    border-radius: 20px;
    background: white;
    box-shadow: 0 8px 24px rgba(15,23,42,0.07);
    margin-bottom: 18px;
    min-height: 145px;
}

.segment-title {
    font-size: 19px;
    font-weight: 700;
    color: #312e81;
}

.segment-text {
    color: #64748b;
    font-size: 14px;
}

/* Insight box */
.insight {
    padding: 20px;
    border-radius: 18px;
    background: linear-gradient(120deg, #fff7ed, #fef3c7);
    border-left: 5px solid #f59e0b;
    margin: 10px 0;
}

/* Login card */
.login-card {
    padding: 35px;
    border-radius: 25px;
    background: rgba(255,255,255,0.92);
    box-shadow: 0 15px 45px rgba(124,58,237,0.15);
}

.small-text {
    color: #64748b;
    font-size: 13px;
}

.footer {
    text-align: center;
    color: #94a3b8;
    padding: 30px;
    font-size: 13px;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# --------------------------------------------------
# LOGIN PAGE
# --------------------------------------------------
if not st.session_state.logged_in:

    st.markdown("<br><br>", unsafe_allow_html=True)

    left, center, right = st.columns([1, 2, 1])

    with center:

        st.markdown("""
        <div class="login-card">
            <div style="text-align:center;">
                <div style="font-size:60px;">🌸</div>
                <div class="main-title" style="font-size:42px;">
                    CustoBloom
                </div>
                <p class="subtitle">
                    Smart Customer Segmentation for Smarter Marketing
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 🔐 Welcome Back!")

        username = st.text_input(
            "👤 Username",
            placeholder="Enter your username"
        )

        password = st.text_input(
            "🔑 Password",
            type="password",
            placeholder="Enter your password"
        )

        if st.button("✨ Login to CustoBloom", use_container_width=True):

            if username == "admin" and password == "admin123":
                st.session_state.logged_in = True
                st.success("Login successful! Welcome to CustoBloom 🌸")
                st.rerun()

            else:
                st.error("Invalid username or password.")

        st.info("Demo Login  •  Username: admin  •  Password: admin123")


# --------------------------------------------------
# MAIN WEBSITE
# --------------------------------------------------
else:

    # SIDEBAR
    with st.sidebar:

        st.markdown("""
        <div style="text-align:center;">
            <div style="font-size:45px;">🌸</div>
            <h2 style="color:#7c3aed;">CustoBloom</h2>
            <p style="color:#64748b;">
                AI-Powered Marketing
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        page = st.radio(
            "Navigation",
            [
                "🏠 Dashboard",
                "👥 Customers",
                "🤖 Segmentation",
                "📊 Analytics",
                "💡 Smart Insights",
                "ℹ️ About"
            ]
        )

        st.divider()

        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()


    # --------------------------------------------------
    # DASHBOARD
    # --------------------------------------------------
    if page == "🏠 Dashboard":

        st.markdown(
            '<div class="main-title">CustoBloom 🌸</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="subtitle">Smart Customer Segmentation for Smarter Marketing</div>',
            unsafe_allow_html=True
        )

        st.markdown("""
        <div class="welcome-box">
            <div class="welcome-title">✨ Welcome to your Customer Intelligence Hub</div>
            <div class="welcome-text">
                Discover customer behaviour, identify valuable segments
                and make smarter marketing decisions using Machine Learning.
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
                <div class="metric-icon">🤖</div>
                <div class="metric-number">K-Means</div>
                <div class="metric-label">ML Algorithm</div>
            </div>
            """, unsafe_allow_html=True)

        with c4:
            st.markdown("""
            <div class="metric-card">
                <div class="metric-icon">📈</div>
                <div class="metric-number">AI</div>
                <div class="metric-label">Smart Analytics</div>
            </div>
            """, unsafe_allow_html=True)


        st.markdown("## 🎯 Customer Segments")

        s1, s2 = st.columns(2)

        with s1:
            st.markdown("""
            <div class="segment-card">
                <div class="segment-title">💎 Premium Customers</div>
                <div class="segment-text">
                    High-value customers with strong purchasing behaviour.
                    Perfect for personalised premium offers.
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="segment-card">
                <div class="segment-title">💰 High-Income Low Spenders</div>
                <div class="segment-text">
                    Customers with high income but lower spending.
                    Target them with personalised campaigns.
                </div>
            </div>
            """, unsafe_allow_html=True)

        with s2:
            st.markdown("""
            <div class="segment-card">
                <div class="segment-title">🛍️ Regular Customers</div>
                <div class="segment-text">
                    Customers with consistent purchasing behaviour.
                    Encourage them with loyalty rewards.
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="segment-card">
                <div class="segment-title">⭐ Loyal Customers</div>
                <div class="segment-text">
                    Highly engaged customers who can become
                    long-term brand advocates.
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("## 💡 Quick Marketing Tip")

        st.markdown("""
        <div class="insight">
            <b>🎯 Personalisation is the key!</b><br>
            Different customer segments respond to different marketing
            strategies. Use segmentation to deliver the right message
            to the right customer.
        </div>
        """, unsafe_allow_html=True)


    # --------------------------------------------------
    # CUSTOMERS PAGE
    # --------------------------------------------------
    elif page == "👥 Customers":

        st.markdown(
            '<div class="main-title">👥 Customer Data</div>',
            unsafe_allow_html=True
        )

        st.write(
            "Explore and understand your customer base."
        )

        customer_data = {
            "Customer ID": [1, 2, 3, 4, 5],
            "Age": [19, 21, 25, 31, 40],
            "Annual Income": [15000, 35000, 45000, 60000, 80000],
            "Spending Score": [39, 81, 77, 40, 65]
        }

        st.dataframe(
            customer_data,
            use_container_width=True
        )

        st.info(
            "📌 The complete dataset will be connected to this page next."
        )


    # --------------------------------------------------
    # SEGMENTATION PAGE
    # --------------------------------------------------
    elif page == "🤖 Segmentation":

        st.markdown(
            '<div class="main-title">🤖 K-Means Segmentation</div>',
            unsafe_allow_html=True
        )

        st.write(
            "Use Machine Learning to group customers according to similar behaviour."
        )

        st.markdown("### 🎯 Selected Algorithm")

        st.success("K-Means Clustering")

        st.markdown("### 📌 Current Segments")

        segments = [
            "💎 Premium Customers",
            "🛍️ Regular Customers",
            "💰 High-Income Low Spenders",
            "⭐ Loyal Customers"
        ]

        for segment in segments:
            st.write("• " + segment)

        st.warning(
            "🚀 Actual K-Means prediction will be connected to the customer dataset in the next stage."
        )


    # --------------------------------------------------
    # ANALYTICS PAGE
    # --------------------------------------------------
    elif page == "📊 Analytics":

        st.markdown(
            '<div class="main-title">📊 Analytics</div>',
            unsafe_allow_html=True
        )

        st.write("Customer analytics and visual insights.")

        chart_data = {
            "Segment": [
                "Premium",
                "Regular",
                "High-Income Low Spenders",
                "Loyal"
            ],
            "Customers": [45, 70, 35, 50]
        }

        st.bar_chart(
            chart_data,
            x="Segment",
            y="Customers"
        )

        st.info(
            "📈 More interactive analytics will be connected with the real dataset next."
        )


    # --------------------------------------------------
    # SMART INSIGHTS
    # --------------------------------------------------
    elif page == "💡 Smart Insights":

        st.markdown(
            '<div class="main-title">💡 Smart Marketing Insights</div>',
            unsafe_allow_html=True
        )

        insights = [
            ("💎 Premium Customers",
             "Provide personalised premium offers and exclusive benefits."),

            ("🛍️ Regular Customers",
             "Use loyalty points, discounts and repeat-purchase campaigns."),

            ("💰 High-Income Low Spenders",
             "Try personalised recommendations and targeted promotions."),

            ("⭐ Loyal Customers",
             "Focus on retention, rewards and referral campaigns.")
        ]

        for title, text in insights:

            st.markdown(f"""
            <div class="insight">
                <b>{title}</b><br>
                {text}
            </div>
            """, unsafe_allow_html=True)


    # --------------------------------------------------
    # ABOUT
    # --------------------------------------------------
    elif page == "ℹ️ About":

        st.markdown(
            '<div class="main-title">ℹ️ About CustoBloom</div>',
            unsafe_allow_html=True
        )

        st.write("""
        **CustoBloom** is a smart customer segmentation platform
        designed to help businesses understand their customers better.

        The system uses Machine Learning, particularly **K-Means
        Clustering**, to group customers according to similar
        characteristics and purchasing behaviour.
        """)

        st.markdown("### 🛠️ Technology")

        st.write("""
        - 🐍 Python
        - 🎈 Streamlit
        - 🤖 Machine Learning
        - 📊 Data Analytics
        - 🎯 K-Means Clustering
        """)

        st.success("CustoBloom — Turning customer data into smarter decisions 🌸")


    # FOOTER
    st.markdown("""
    <div class="footer">
        🌸 CustoBloom • Smart Customer Segmentation • AI-Powered Marketing
    </div>
    """, unsafe_allow_html=True)
