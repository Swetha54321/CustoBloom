

# =========================================================
# PAGE SETTINGS
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
@@ -21,28 +21,37 @@
# DATABASE
# =========================================================

def create_database():
def get_database():

conn = sqlite3.connect("users.db")

cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            email TEXT NOT NULL,
            password TEXT NOT NULL
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS users "
        "(username TEXT PRIMARY KEY, password TEXT NOT NULL)"
    )

    # Add email column if it does not already exist
    cursor.execute("PRAGMA table_info(users)")

    columns = [row[1] for row in cursor.fetchall()]

    if "email" not in columns:

        cursor.execute(
            "ALTER TABLE users ADD COLUMN email TEXT"
)
    """)

conn.commit()
    conn.close()

    return conn


def hash_password(password):

return hashlib.sha256(
        password.encode()
        password.encode("utf-8")
).hexdigest()


@@ -53,71 +62,70 @@ def valid_email(email):
return re.match(pattern, email) is not None


def register_user(username, email, password):
def create_account(username, email, password):

    conn = sqlite3.connect("users.db")
    conn = get_database()

cursor = conn.cursor()

    try:
    cursor.execute(
        "SELECT username FROM users WHERE username = ?",
        (username,)
    )

        cursor.execute(
            """
            INSERT INTO users
            (username, email, password)
            VALUES (?, ?, ?)
            """,
            (
                username,
                email,
                hash_password(password)
            )
        )
    existing_user = cursor.fetchone()

    if existing_user is not None:

        conn.commit()
        conn.close()

        success = True
        return False

    except sqlite3.IntegrityError:
    cursor.execute(
        "INSERT INTO users (username, email, password) "
        "VALUES (?, ?, ?)",
        (
            username,
            email,
            hash_password(password)
        )
    )

        success = False
    conn.commit()

conn.close()

    return success
    return True


def check_login(username, password):
def login_user(username, password):

    conn = sqlite3.connect("users.db")
    conn = get_database()

cursor = conn.cursor()

cursor.execute(
        """
        SELECT *
        FROM users
        WHERE username = ?
        AND password = ?
        """,
        "SELECT username FROM users "
        "WHERE username = ? AND password = ?",
(
username,
hash_password(password)
)
)

    user = cursor.fetchone()
    result = cursor.fetchone()

conn.close()

    return user is not None
    return result is not None


create_database()
# Create database
get_database().close()


# =========================================================
# SESSION STATE
# SESSION
# =========================================================

if "logged_in" not in st.session_state:
@@ -126,61 +134,70 @@ def check_login(username, password):


# =========================================================
# CUSTOM CSS
# DESIGN
# =========================================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #0f172a, #172554);
    color: white;
}

.main-title {
    font-size: 40px;
    font-weight: bold;
    color: #60a5fa;
}

.subtitle {
    color: #cbd5e1;
    font-size: 18px;
}

.card {
    background: #1e293b;
    padding: 25px;
    border-radius: 18px;
    border: 1px solid #334155;
    margin-bottom: 15px;
}

.offer {
    background: #172554;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #3b82f6;
    margin-bottom: 12px;
}

</style>
""", unsafe_allow_html=True)
st.markdown(
    """
    <style>

    .stApp {
        background: linear-gradient(
            135deg,
            #0f172a,
            #172554
        );
        color: white;
    }

    .title {
        font-size: 42px;
        font-weight: bold;
        color: #60a5fa;
    }

    .subtitle {
        font-size: 18px;
        color: #cbd5e1;
    }

    .card {
        background: #1e293b;
        padding: 22px;
        border-radius: 18px;
        border: 1px solid #334155;
        margin-bottom: 15px;
    }

    .offer {
        background: #172554;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #3b82f6;
        margin-bottom: 15px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# LOGIN / SIGN UP PAGE
# LOGIN / SIGN UP
# =========================================================

if not st.session_state.logged_in:

st.markdown(
        "<h1 class='main-title'>🛍️ Smart Customer Segmentation</h1>",
        "<h1 class='title'>🛍️ Smart Customer Segmentation</h1>",
unsafe_allow_html=True
)

st.markdown(
        "<p class='subtitle'>Turn customer data into smart business decisions.</p>",
        "<p class='subtitle'>"
        "Turn customer data into smart business decisions."
        "</p>",
unsafe_allow_html=True
)

@@ -199,15 +216,15 @@ def check_login(username, password):

st.subheader("🔐 Login to Dashboard")

        username = st.text_input(
        login_username = st.text_input(
"👤 Username",
            key="login_username"
            key="login_user"
)

        password = st.text_input(
        login_password = st.text_input(
"🔒 Password",
type="password",
            key="login_password"
            key="login_pass"
)

if st.button(
@@ -216,17 +233,17 @@ def check_login(username, password):
):

if (
                username.strip() == ""
                or password.strip() == ""
                login_username.strip() == ""
                or login_password == ""
):

st.warning(
"⚠️ Please enter username and password."
)

            elif check_login(
                username.strip(),
                password
            elif login_user(
                login_username.strip(),
                login_password
):

st.session_state.logged_in = True
@@ -254,38 +271,37 @@ def check_login(username, password):

new_username = st.text_input(
"👤 Create Username",
            key="signup_username"
            key="new_user"
)

new_email = st.text_input(
"📧 Email Address",
            key="signup_email"
            key="new_email"
)

new_password = st.text_input(
"🔒 Create Password",
type="password",
            key="signup_password"
            key="new_pass"
)

confirm_password = st.text_input(
"🔒 Confirm Password",
type="password",
            key="confirm_password"
            key="confirm_pass"
)

if st.button(
"✨ Create Account",
use_container_width=True
):

            username_clean = new_username.strip()

            email_clean = new_email.strip()
            username = new_username.strip()
            email = new_email.strip()

if (
                username_clean == ""
                or email_clean == ""
                username == ""
                or email == ""
or new_password == ""
or confirm_password == ""
):
@@ -294,7 +310,7 @@ def check_login(username, password):
"⚠️ Please fill all fields."
)

            elif not valid_email(email_clean):
            elif not valid_email(email):

st.error(
"❌ Please enter a valid email address."
@@ -303,7 +319,7 @@ def check_login(username, password):
elif len(new_password) < 4:

st.warning(
                    "⚠️ Password should contain at least 4 characters."
                    "⚠️ Password must contain at least 4 characters."
)

elif new_password != confirm_password:
@@ -314,24 +330,27 @@ def check_login(username, password):

else:

                created = register_user(
                    username_clean,
                    email_clean,
                account_created = create_account(
                    username,
                    email,
new_password
)

                if created:
                if account_created:

st.success(
                        "🎉 Account created successfully! "
                        "You can now login."
                        "🎉 Account created successfully!"
                    )

                    st.info(
                        "Now open the Login tab and login "
                        "with your new account."
)

else:

st.error(
                        "❌ Username already exists. "
                        "Please choose another username."
                        "❌ Username already exists."
)


@@ -342,56 +361,70 @@ def check_login(username, password):
else:

st.markdown(
        "<h1 class='main-title'>📊 Customer Segmentation Dashboard</h1>",
        "<h1 class='title'>"
        "📊 Customer Segmentation Dashboard"
        "</h1>",
unsafe_allow_html=True
)

    st.write(
    st.markdown(
        "<p class='subtitle'>"
"Welcome to your Smart Customer Segmentation System! 👋"
        "</p>",
        unsafe_allow_html=True
)

st.markdown("---")


# =====================================================
    # TOP CARDS
    # FEATURE CARDS
# =====================================================

col1, col2, col3 = st.columns(3)

with col1:

        st.markdown("""
        <div class="card">
        <h2>📁 Upload Dataset</h2>
        <p>Upload your customer CSV data.</p>
        </div>
        """, unsafe_allow_html=True)
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

        st.markdown("""
        <div class="card">
        <h2>🎯 K-Means Groups</h2>
        <p>Automatically discover customer segments.</p>
        </div>
        """, unsafe_allow_html=True)
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

        st.markdown("""
        <div class="card">
        <h2>🤖 Smart Offers</h2>
        <p>Get targeted marketing suggestions.</p>
        </div>
        """, unsafe_allow_html=True)
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
    # UPLOAD DATASET
    # CSV UPLOAD
# =====================================================

st.subheader("📂 Upload Customer Dataset")
@@ -410,7 +443,11 @@ def check_login(username, password):
df.columns
.astype(str)
.str.strip()
            .str.replace("\ufeff", "", regex=False)
            .str.replace(
                "\ufeff",
                "",
                regex=False
            )
)

df = df.reset_index(drop=True)
@@ -421,7 +458,7 @@ def check_login(username, password):


# =================================================
        # DATASET PREVIEW
        # DATA PREVIEW
# =================================================

st.subheader("👀 Dataset Preview")
@@ -435,35 +472,35 @@ def check_login(username, password):


# =================================================
        # FIND REQUIRED COLUMNS
        # FIND COLUMNS
# =================================================

income_column = None

spending_column = None


for column in df.columns:

            name = str(column).lower().strip()
            column_name = str(
                column
            ).lower().strip()

if (
                "annual" in name
                and "income" in name
                "annual" in column_name
                and "income" in column_name
):

income_column = column

if (
                "spending" in name
                and "score" in name
                "spending" in column_name
                and "score" in column_name
):

spending_column = column


# =================================================
        # CUSTOMER SEGMENTATION
        # CHECK COLUMNS
# =================================================

if (
@@ -475,6 +512,7 @@ def check_login(username, password):
"🎯 Customer Segmentation"
)


if st.button(
"🚀 Run Customer Segmentation",
use_container_width=True
@@ -490,6 +528,7 @@ def check_login(username, password):
errors="coerce"
)


valid_data = df[
[
"Income_Value",
@@ -506,7 +545,9 @@ def check_login(username, password):

else:

                    # =====================================
# K-MEANS
                    # =====================================

model = KMeans(
n_clusters=4,
@@ -519,11 +560,12 @@ def check_login(username, password):
)


                    # =====================================
# GROUP ASSIGNMENT
                    # =====================================

df["Customer Group"] = "Not Available"


for index, cluster in zip(
valid_data.index,
cluster_numbers
@@ -532,17 +574,20 @@ def check_login(username, password):
df.at[
index,
"Customer Group"
                        ] = "Group " + str(cluster + 1)
                        ] = (
                            "Group "
                            + str(cluster + 1)
                        )


st.success(
"🎉 Customer segmentation completed successfully!"
)


                    # =================================================
                    # CUSTOMER GROUPS
                    # =================================================
                    # =====================================
                    # RESULTS
                    # =====================================

st.subheader(
"👥 Customer Groups"
@@ -554,9 +599,9 @@ def check_login(username, password):
)


                    # =================================================
                    # CLUSTER CENTERS
                    # =================================================
                    # =====================================
                    # CENTERS
                    # =====================================

centers = model.cluster_centers_

@@ -569,69 +614,67 @@ def check_login(username, password):
].mean()


                    # =================================================
                    # GROUP SUMMARY
                    # =================================================
                    # =====================================
                    # SUMMARY
                    # =====================================

st.subheader(
"📊 Customer Group Summary"
)

summary_data = []


for cluster in range(4):

                        cluster_income = centers[
                        income = centers[
cluster
][0]

                        cluster_spending = centers[
                        spending = centers[
cluster
][1]

                        customer_count = (
                        count = (
cluster_numbers == cluster
).sum()


                        summary_data.append({

                            "Group":
                                "Group "
                                + str(cluster + 1),

                            "Customers":
                                int(customer_count),

                            "Avg Income":
                                round(
                                    cluster_income,
                                    2
                                ),

                            "Avg Spending Score":
                                round(
                                    cluster_spending,
                                    2
                                )
                        })
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


                    # =================================================
                    # =====================================
# BAR CHART
                    # =================================================
                    # =====================================

st.subheader(
"📈 Customers in Each Group"
@@ -644,7 +687,6 @@ def check_login(username, password):
]
].set_index("Group")


st.bar_chart(
chart_data
)
@@ -653,22 +695,14 @@ def check_login(username, password):
st.markdown("---")


                    # =================================================
                    # SMART INSIGHTS
                    # =================================================
                    # =====================================
                    # FIND CUSTOMER TYPES
                    # =====================================

                    st.subheader(
                        "🤖 Smart Customer Insights"
                    )


                    high_income_high_spending = None

                    high_income_low_spending = None

                    low_income_high_spending = None

                    low_income_low_spending = None
                    vip_group = None
                    potential_group = None
                    deal_group = None
                    growth_group = None


for cluster in range(4):
@@ -693,89 +727,180 @@ def check_login(username, password):
spending >= average_spending
):

                            high_income_high_spending = (
                                group_name
                            )
                            vip_group = group_name

elif (
income >= average_income
and
spending < average_spending
):

                            high_income_low_spending = (
                                group_name
                            )
                            potential_group = group_name

elif (
income < average_income
and
spending >= average_spending
):

                            low_income_high_spending = (
                                group_name
                            )
                            deal_group = group_name

else:

                            low_income_low_spending = (
                                group_name
                            )
                            growth_group = group_name


                    # =================================================
                    # =====================================
# SMART OFFERS
                    # =================================================
                    # =====================================

                    st.subheader(
                        "🤖 Smart Customer Insights"
                    )

st.subheader(
"💡 Smart Offers & Marketing Ideas"
)


                    if high_income_high_spending is not None:
                    if vip_group is not None:

st.markdown(
                            f"""
                            """
                           <div class="offer">

                            <h3>
                            💎 VIP Champions —
                            {high_income_high_spending}
                            </h3>

                            <h3>💎 VIP Champions</h3>
                           <p>
                            These customers have high income
                            and high spending behaviour.
                            High income and high spending customers.
                           </p>

                           <b>🎁 Offer:</b>
                           Premium products, loyalty rewards
                           and exclusive early access.

                           <br><br>

                           <b>📢 Strategy:</b>
                            Build long-term loyalty with VIP experiences.
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


                    if high_income_low_spending is not None:
                    if deal_group is not None:

st.markdown(
                            f"""
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


                            <h3>
                            🌟 Hidden Potential —
                            {high_income_low_spending}
                            </h3>
                    if growth_group is not None:

                        st.markdown(
                            """
                            <div class="offer">
                            <h3>🌱 Growth Customers</h3>
                           <p>
                            These customers have strong purchasing
                            capacity but lower spending.
                            </
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
