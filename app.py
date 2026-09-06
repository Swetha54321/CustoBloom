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
# LAVENDER DESIGN
# =========================================================

st.markdown(
    """
    <style>

    /* Main background */
    .stApp {
        background: #F3EEFF;
        color: #24143D;
    }

    /* Main headings */
    .title {
        font-size: 42px;
        font-weight: bold;
        color: #4C1D95 !important;
    }

    /* Subtitle */
    .subtitle {
        font-size: 18px;
        color: #3B3150 !important;
    }

    /* Normal Streamlit text */
    .stApp p,
    .stApp label,
    .stApp span,
    .stApp div {
        color: #24143D;
    }

    /* Input labels */
    div[data-testid="stTextInput"] label,
    div[data-testid="stTextInput"] label p {
        color: #24143D !important;
        font-weight: 700 !important;
    }

    /* Input boxes */
    div[data-testid="stTextInput"] input {
        background-color: #FFFFFF !important;
        color: #24143D !important;
        border: 2px solid #C4B5FD !important;
        border-radius: 10px !important;
    }

    /* Placeholder */
    div[data-testid="stTextInput"] input::placeholder {
        color: #6B5B7A !important;
        opacity: 1 !important;
    }

    /* Cards */
    .card {
        background: #FFFFFF;
        padding: 22px;
        border-radius: 18px;
        border: 2px solid #DDD6FE;
        margin-bottom: 15px;
        box-shadow: 0 4px 12px rgba(76, 29, 149, 0.08);
    }

    .card h2 {
        color: #4C1D95 !important;
    }

    .card p {
        color: #3B3150 !important;
    }

    /* Offer cards */
    .offer {
        background: #FFFFFF;
        padding: 20px;
        border-radius: 15px;
        border: 2px solid #C4B5FD;
        margin-bottom: 15px;
        box-shadow: 0 4px 12px rgba(76, 29, 149, 0.08);
    }

    .offer h3 {
        color: #5B21B6 !important;
    }

    .offer p,
    .offer b {
        color: #312E3A !important;
    }

    /* Buttons */
    .stButton > button {
        background-color: #6D28D9 !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
    }

    .stButton > button:hover {
        background-color: #5B21B6 !important;
        color: #FFFFFF !important;
    }

    /* Tabs */
    button[data-baseweb="tab"] {
        color: #4C1D95 !important;
        font-weight: 700 !important;
    }

    /* File uploader */
    section[data-testid="stFileUploaderDropzone"] {
        background: #FFFFFF !important;
        border: 2px dashed #A78BFA !important;
        border-radius: 12px !important;
    }

    /* Dataframes */
    div[data-testid="stDataFrame"] {
        border: 2px solid #DDD6FE;
        border-radius: 10px;
    }

    /* Download button */
    .stDownloadButton > button {
        background-color: #6D28D9 !important;
        color: #FFFFFF !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
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
                    # K-MEANS
                    # =====================================

                    model = KMeans(
                        n_clusters=4,
                        random_state=42,
                        n_init=10
                    )

                    cluster_numbers = model.fit_predict(
                        valid_data
                    )


                    # =====================================
                    # GROUP ASSIGNMENT
                    # =====================================

                    df["Customer Group"] = "Not Available"

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
                        "🎉 Customer segmentation completed successfully!"
                    )


                    # =====================================
                    # RESULTS
                    # =====================================

                    st.subheader(
                        "👥 Customer Groups"
                    )

                    st.dataframe(
                        df,
                        use_container_width=True
                    )


                    # =====================================
                    # CENTERS
                    # =====================================

                    centers = model.cluster_centers_

                    average_income = valid_data[
                        "Income_Value"
                    ].mean()

                    average_spending = valid_data[
                        "Spending_Value"
                    ].mean()


                    # =====================================
                    # SUMMARY
                    # =====================================

                    st.subheader(
                        "📊 Customer Group Summary"
                    )

                    summary_data = []

                    for cluster in range(4):

                        income = centers[
                            cluster
                        ][0]

                        spending = centers[
                            cluster
                        ][1]

                        count = (
                            cluster_numbers == cluster
                        ).sum()

                        summary_data.append(
                            {
                                "Group":
                                    "Group "
                                    + str(cluster + 1),

                                "Customers":
                                    int(count),

                                "Avg Income":
                                    round(
                                        income,
                                        2
                                    ),

                                "Avg Spending Score":
                                    round(
                                        spending,
                                        2
                                    )
                            }
                        )


                    summary_df = pd.DataFrame(
                        summary_data
                    )

                    st.dataframe(
                        summary_df,
                        use_container_width=True
                    )


                    # =====================================
                    # BAR CHART
                    # =====================================

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


                    # =====================================
                    # FIND CUSTOMER TYPES
                    # =====================================

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


                    # =====================================
                    # SMART OFFERS
                    # =====================================

                    st.subheader(
                        "🤖 Smart Customer Insights"
                    )

                    st.subheader(
                        "💡 Smart Offers & Marketing Ideas"
                    )


                    if vip_group is not None:

                        st.markdown(
                            """
                            <div class="offer">
                            <h3>💎 VIP Champions</h3>
                            <p>
                            High income and high spending customers.
                            </p>
                            <b>🎁 Offer:</b>
                            Premium products, loyalty rewards
                            and exclusive early access.
                            <br><br>
                            <b>📢 Strategy:</b>
                            Build long-term customer loyalty.
                            </div>
                            """,
                            unsafe_allow_html=True
                        )


                    if potential_group is not None:

                        st.markdown(
                            """
                            <div class="offer">
                            <h3>🌟 Hidden Potential</h3>
                            <p>
                            High income but lower spending customers.
                            </p>
                            <b>🎁 Offer:</b>
                            Personalised discounts,
                            recommendations and trial offers.
                            <br><br>
                            <b>📢 Strategy:</b>
                            Encourage more frequent purchases.
                            </div>
                            """,
                            unsafe_allow_html=True
                        )


                    if deal_group is not None:

                        st.markdown(
                            """
                            <div class="offer">
                            <h3>🔥 Deal Lovers</h3>
                            <p>
                            Lower income but active spending customers.
                            </p>
                            <b>🎁 Offer:</b>
                            Bundle deals, value packs
                            and limited-time offers.
                            <br><br>
                            <b>📢 Strategy:</b>
                            Reward their engagement.
                            </div>
                            """,
                            unsafe_allow_html=True
                        )


                    if growth_group is not None:

                        st.markdown(
                            """
                            <div class="offer">
                            <h3>🌱 Growth Customers</h3>
                            <p>
                            Lower income and lower spending customers.
                            </p>
                            <b>🎁 Offer:</b>
                            Welcome offers, affordable bundles
                            and first-purchase incentives.
                            <br><br>
                            <b>📢 Strategy:</b>
                            Encourage first and repeat purchases.
                            </div>
                            """,
                            unsafe_allow_html=True
                        )


                    # =====================================
                    # DOWNLOAD
                    # =====================================

                    st.markdown("---")

                    st.subheader(
                        "📥 Download Segmented Customer Report"
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
                        label="📥 Download CSV Report",
                        data=csv_data,
                        file_name="customer_segments.csv",
                        mime="text/csv",
                        use_container_width=True
                    )


        else:

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


    # =====================================================
    # LOGOUT
    # =====================================================

    st.markdown("---")

    if st.button("🚪 Logout"):

        st.session_state.logged_in = False

        st.rerun()
