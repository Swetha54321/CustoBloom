import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="CustoBloom",
    page_icon="🌺",
    layout="wide",
    initial_sidebar_state="expanded"
)

CSS = (
    "<style>"
    ".stApp{background:linear-gradient(135deg,#050816 0%,#11152f 45%,#1b1030 100%);color:#f8fafc;}"
    "[data-testid='stSidebar']{background:linear-gradient(180deg,#080b1d,#140d25);border-right:1px solid #33264f;}"
    "[data-testid='stSidebar'] *{color:#e8e8f0;}"
    "html,body,[class*='css']{font-family:Arial,sans-serif;}"
    ".hero{text-align:center;padding:35px 10px 20px;}"
    ".flower{font-size:72px;line-height:1;margin-bottom:8px;}"
    ".brand{font-family:Georgia,serif;font-size:48px;font-weight:900;"
    "background:linear-gradient(90deg,#f9a8d4,#c084fc,#818cf8);"
    "-webkit-background-clip:text;-webkit-text-fill-color:transparent;}"
    ".tagline{color:#aab4cf;font-size:17px;margin-top:5px;}"
    ".panel{background:rgba(20,18,43,.88);border:1px solid #33264f;"
    "border-radius:22px;padding:24px;margin:12px 0;box-shadow:0 12px 35px rgba(0,0,0,.25);}"
    ".metric{background:linear-gradient(145deg,rgba(34,29,67,.95),rgba(18,19,43,.95));"
    "border:1px solid #382d58;border-radius:18px;padding:20px;min-height:130px;}"
    ".metric-icon{font-size:32px;}"
    ".metric-value{font-size:28px;font-weight:800;color:#fff;margin-top:6px;}"
    ".metric-label{font-size:13px;color:#aab4cf;}"
    ".section-title{font-size:28px;font-weight:800;color:#fff;margin-top:25px;}"
    ".segment{background:rgba(28,24,57,.9);border:1px solid #382d58;border-radius:18px;padding:20px;min-height:180px;}"
    ".segment h3{color:#f3e8ff;margin:8px 0;}"
    ".segment p{color:#aab4cf;}"
    ".footer{text-align:center;color:#707b96;padding:30px 0 10px;font-size:13px;}"
    ".stButton>button{border:0;border-radius:12px;background:linear-gradient(90deg,#8b5cf6,#ec4899);"
    "color:white;font-weight:800;min-height:44px;}"
    ".stButton>button:hover{background:linear-gradient(90deg,#a78bfa,#f472b6);color:white;}"
    ".stTextInput input{background:#0b0e21!important;color:#fff!important;border:1px solid #3a3155!important;border-radius:12px!important;}"
    "</style>"
)

st.markdown(CSS, unsafe_allow_html=True)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:

    st.markdown(
        '<div class="hero">'
        '<div class="flower">🌺</div>'
        '<div class="brand">CustoBloom</div>'
        '<div class="tagline">Smart Customer Segmentation for Smarter Marketing</div>'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="panel">'
        '<h2 style="color:#fff;text-align:center;">Welcome Back 👋</h2>'
        '<p style="color:#aab4cf;text-align:center;">Sign in to explore your customer intelligence dashboard.</p>'
        '</div>',
        unsafe_allow_html=True
    )

    left, center, right = st.columns([1, 2, 1])

    with center:
        username = st.text_input("Username", placeholder="Enter username")
        password = st.text_input("Password", type="password", placeholder="Enter password")

        if st.button("🌸 Enter CustoBloom", use_container_width=True):
            if username == "admin" and password == "admin123":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Incorrect username or password.")

        st.caption("Demo login: admin / admin123")

    st.markdown(
        '<div class="footer">CustoBloom • AI-powered customer intelligence</div>',
        unsafe_allow_html=True
    )

    st.stop()

with st.sidebar:

    st.markdown(
        '<div style="text-align:center;padding:15px 0 25px;">'
        '<div style="font-size:48px;">🌺</div>'
        '<div style="font-family:Georgia,serif;font-size:27px;font-weight:800;color:#e9d5ff;">CustoBloom</div>'
        '<div style="font-size:10px;color:#8f9ab5;letter-spacing:2px;">CUSTOMER INTELLIGENCE</div>'
        '</div>',
        unsafe_allow_html=True
    )

    page = st.radio(
        "NAVIGATION",
        [
            "🏠 Dashboard",
            "👥 Customers",
            "🎯 Segmentation",
            "📊 Analytics",
            "💡 Smart Insights",
            "ℹ️ About"
        ]
    )

    st.markdown("---")

    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

if page == "🏠 Dashboard":

    st.markdown(
        '<div class="hero">'
        '<div class="flower">🌺</div>'
        '<div class="brand">CustoBloom</div>'
        '<div class="tagline">Turn customer data into smarter marketing decisions.</div>'
        '</div>',
        unsafe_allow_html=True
    )

    cols = st.columns(4)

    metrics = [
        ("👥", "200", "Total Customers"),
        ("🎯", "4", "Customer Segments"),
        ("🧠", "K-Means", "ML Algorithm"),
        ("📈", "94%", "Insight Score")
    ]

    for col, item in zip(cols, metrics):

        icon, value, label = item

        with col:

            st.markdown(
                '<div class="metric">'
                '<div class="metric-icon">' + icon + '</div>'
                '<div class="metric-value">' + value + '</div>'
                '<div class="metric-label">' + label + '</div>'
                '</div>',
                unsafe_allow_html=True
            )

    st.markdown(
        '<div class="section-title">🌸 Customer Segments</div>',
        unsafe_allow_html=True
    )

    segments = [
        ("💎", "Premium Customers", "High income and high spending. Best suited for exclusive offers.", "High"),
        ("🛍️", "Regular Customers", "Stable purchasing behaviour. Grow engagement with loyalty rewards.", "Medium"),
        ("💰", "High-Income Low Spenders", "Strong purchasing power with an opportunity to increase spending.", "High"),
        ("❤️", "Loyal Customers", "Consistent customers. Focus on retention and appreciation.", "Very High")
    ]

    cols = st.columns(4)

    for col, item in zip(cols, segments):

        icon, title, description, priority = item

        with col:

            st.markdown(
                '<div class="segment">'
                '<div style="font-size:35px;">' + icon + '</div>'
                '<h3>' + title + '</h3>'
                '<p>' + description + '</p>'
                '<p><b style="color:#d8b4fe;">Priority:</b> ' + priority + '</p>'
                '</div>',
                unsafe_allow_html=True
            )

    st.markdown(
        '<div class="panel">'
        '<h3 style="color:#e9d5ff;">✨ Smart Marketing Opportunity</h3>'
        '<p style="color:#aab4cf;">Personalise campaigns by customer segment instead of sending the same offer to everyone.</p>'
        '</div>',
        unsafe_allow_html=True
    )

elif page == "👥 Customers":

    st.markdown(
        '<div class="brand">Customer Explorer</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="tagline">Explore sample customer information.</div>',
        unsafe_allow_html=True
    )

    df = pd.DataFrame({
        "Customer ID": [1, 2, 3, 4, 5, 6, 7, 8],
        "Gender": ["Male", "Female", "Female", "Male", "Female", "Male", "Female", "Male"],
        "Age": [19, 21, 25, 31, 35, 40, 45, 50],
        "Annual Income": [15000, 18000, 25000, 45000, 55000, 65000, 80000, 100000],
        "Spending Score": [39, 81, 65, 55, 72, 45, 30, 20]
    })

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    st.markdown(
        '<div class="panel">'
        '<h3 style="color:#e9d5ff;">🔎 What to look for</h3>'
        '<p style="color:#aab4cf;">Income and spending score can help identify different customer behaviour patterns.</p>'
        '</div>',
        unsafe_allow_html=True
    )

elif page == "🎯 Segmentation":

    st.markdown(
        '<div class="brand">AI Segmentation</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="tagline">Understand customer groups using clustering.</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="panel">'
        '<h2 style="color:#fff;">🧠 K-Means Clustering</h2>'
        '<p style="color:#aab4cf;">K-Means groups customers with similar characteristics, such as annual income and spending score.</p>'
        '</div>',
        unsafe_allow_html=True
    )

    seg_df = pd.DataFrame({
        "Segment": ["Premium", "Regular", "High Income - Low Spend", "Loyal"],
        "Customers": [48, 62, 35, 55],
        "Priority": ["Very High", "Medium", "High", "Very High"]
    })

    st.dataframe(
        seg_df,
        use_container_width=True,
        hide_index=True
    )

    st.info(
        "Current dashboard uses demonstration segment values. "
        "The next project step can connect the real dataset and train K-Means."
    )

elif page == "📊 Analytics":

    st.markdown(
        '<div class="brand">Analytics</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="tagline">Visualise customer segment performance.</div>',
        unsafe_allow_html=True
    )

    chart = pd.DataFrame(
        {"Customers": [48, 62, 35, 55]},
        index=["Premium", "Regular", "High Income", "Loyal"]
    )

    st.subheader("👥 Customers by Segment")

    st.bar_chart(chart)

    spending = pd.DataFrame(
        {"Spending Score": [82, 58, 25, 74]},
        index=["Premium", "Regular", "High Income", "Loyal"]
    )

    st.subheader("💸 Average Spending Behaviour")

    st.line_chart(spending)

elif page == "💡 Smart Insights":

    st.markdown(
        '<div class="brand">Smart Insights</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="tagline">Simple actions generated from customer behaviour.</div>',
        unsafe_allow_html=True
    )

    insights = [
        ("💎 Premium Customers", "Recommend premium products and exclusive campaigns."),
        ("🛍️ Regular Customers", "Use loyalty points, bundles and seasonal promotions."),
        ("💰 High-Income Low Spenders", "Try personalised offers to increase engagement."),
        ("❤️ Loyal Customers", "Reward retention with appreciation and loyalty benefits."),
        ("📢 Overall Strategy", "Deliver the right message to the right customer segment.")
    ]

    for title, text in insights:

        st.markdown(
            '<div class="panel">'
            '<h3 style="color:#e9d5ff;">' + title + '</h3>'
            '<p style="color:#aab4cf;">' + text + '</p>'
            '</div>',
            unsafe_allow_html=True
        )

elif page == "ℹ️ About":

    st.markdown(
        '<div class="brand">About CustoBloom</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="tagline">Smart Customer Segmentation for Smarter Marketing.</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="panel">'
        '<h2 style="color:#fff;">🌺 Our Goal</h2>'
        '<p style="color:#aab4cf;">CustoBloom helps businesses understand customer behaviour and create more targeted marketing strategies.</p>'
        '</div>',
        unsafe_allow_html=True
    )

    a, b, c = st.columns(3)

    with a:

        st.markdown(
            '<div class="metric">'
            '<div class="metric-icon">🐍</div>'
            '<div class="metric-value">Python</div>'
            '<div class="metric-label">Programming</div>'
            '</div>',
            unsafe_allow_html=True
        )

    with b:

        st.markdown(
            '<div class="metric">'
            '<div class="metric-icon">📊</div>'
            '<div class="metric-value">Pandas</div>'
            '<div class="metric-label">Data Analysis</div>'
            '</div>',
            unsafe_allow_html=True
        )

    with c:

        st.markdown(
            '<div class="metric">'
            '<div class="metric-icon">🤖</div>'
            '<div class="metric-value">K-Means</div>'
            '<div class="metric-label">Segmentation</div>'
            '</div>',
            unsafe_allow_html=True
        )

    st.markdown(
        '<div class="footer">🌺 CustoBloom • Smart Customer Intelligence</div>',
        unsafe_allow_html=True
    )
