import streamlit as st
import pandas as pd
import sqlite3
import hashlib
import os
import joblib
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Real Estate Investment Advisor",
    page_icon="🏠",
    layout="wide"
)

# ================= CSS REAL ESTATE DARK TECH THEME =================
st.markdown("""
<style>
.stApp {
    background:
        linear-gradient(rgba(5, 10, 18, 0.88), rgba(5, 10, 18, 0.92)),
        url("https://images.unsplash.com/photo-1560518883-ce09059eeffa?auto=format&fit=crop&w=1600&q=80");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    color: #e5e7eb;
}

.main-header {
    background: rgba(15, 23, 42, 0.88);
    backdrop-filter: blur(12px);
    color: white;
    padding: 32px;
    border-radius: 24px;
    margin-bottom: 24px;
    border: 1px solid rgba(148, 163, 184, 0.35);
    box-shadow: 0 12px 40px rgba(0,0,0,0.45);
}

.main-header h1 {
    font-size: 40px;
    color: #ffffff;
}

.sub-text {
    font-size: 17px;
    color: #cbd5e1;
}

.login-title {
    text-align: center;
    margin-top: 25px;
}

.login-title h1 {
    color: #ffffff;
    font-size: 42px;
}

.login-title h4 {
    color: #cbd5e1;
}

.info-box {
    background: rgba(30, 41, 59, 0.88);
    color: #dbeafe;
    padding: 18px;
    border-radius: 16px;
    margin-top: 20px;
    font-weight: 700;
    border: 1px solid rgba(59, 130, 246, 0.35);
}

.kpi-card {
    background: rgba(15, 23, 42, 0.88);
    padding: 24px;
    border-radius: 20px;
    box-shadow: 0 10px 32px rgba(0,0,0,0.45);
    text-align: center;
    border: 1px solid rgba(148, 163, 184, 0.25);
    border-left: 7px solid #38bdf8;
}

.kpi-card h2 {
    color: #38bdf8;
    font-size: 30px;
}

.kpi-card p {
    font-weight: 800;
    color: #e5e7eb;
}

.section-title {
    background: linear-gradient(90deg, #020617, #0f172a, #0369a1);
    color: white;
    padding: 14px 20px;
    border-radius: 16px;
    font-size: 22px;
    font-weight: 900;
    margin-bottom: 20px;
    border: 1px solid rgba(125, 211, 252, 0.35);
    box-shadow: 0 8px 28px rgba(0,0,0,0.35);
}

div.stButton > button {
    background: linear-gradient(90deg, #0f172a, #0369a1);
    color: white;
    border-radius: 14px;
    height: 46px;
    font-weight: 900;
    border: 1px solid rgba(125, 211, 252, 0.45);
}

div.stButton > button:hover {
    background: linear-gradient(90deg, #0369a1, #0ea5e9);
    color: white;
}

div[data-testid="stPlotlyChart"] {
    background: rgba(15, 23, 42, 0.90);
    border-radius: 20px;
    padding: 14px;
    box-shadow: 0 10px 32px rgba(0,0,0,0.42);
    border: 1px solid rgba(148, 163, 184, 0.25);
}

[data-testid="stDataFrame"] {
    background: rgba(15, 23, 42, 0.88);
    border-radius: 16px;
}

label, .stMarkdown, .stTextInput label, .stNumberInput label, .stSelectbox label {
    color: #e5e7eb !important;
}

.stTextInput input, .stNumberInput input {
    background: rgba(15, 23, 42, 0.88) !important;
    color: white !important;
    border-radius: 12px !important;
    border: 1px solid rgba(148, 163, 184, 0.4) !important;
}

.stSelectbox div {
    color: #0f172a;
}
</style>
""", unsafe_allow_html=True)
# ================= DATABASE =================
conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT UNIQUE,
    password TEXT
)
""")
conn.commit()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def signup_user(name, email, password):
    try:
        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
            (name, email, hash_password(password))
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def login_user(email, password):
    cursor.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (email, hash_password(password))
    )
    return cursor.fetchone()

# ================= SESSION =================
if "login" not in st.session_state:
    st.session_state.login = False

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

if "user" not in st.session_state:
    st.session_state.user = ""

# ================= LOGIN / SIGNUP PAGE =================
if not st.session_state.login:

    st.markdown("""
    <div class="login-title">
        <h1>🏠 Real Estate Investment Advisor</h1>
        <h4>Smart household property analysis for better investment decisions</h4>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 1.4, 1])

    with c2:
        tab1, tab2 = st.tabs(["🔐 Login", "📝 Create Account"])

        with tab1:
            st.subheader("Login to Your Account")

            email = st.text_input("Enter your Email", key="login_email")
            password = st.text_input("Enter your Password", type="password", key="login_password")

            if st.button("Login", use_container_width=True):
                if email == "" or password == "":
                    st.warning("Please enter email and password")
                elif login_user(email, password):
                    st.session_state.login = True
                    st.session_state.user = email
                    st.success("Login Successful ✅")
                    st.rerun()
                else:
                    st.error("Invalid email or password ❌")

            st.markdown("""
            <div class="info-box">
                First time user? Click on <b>Create Account</b> and register with your own email and password.
            </div>
            """, unsafe_allow_html=True)

        with tab2:
            st.subheader("Create New Account")

            name = st.text_input("Full Name", key="name")
            signup_email = st.text_input("Create Email", key="signup_email")
            signup_password = st.text_input("Create Password", type="password", key="signup_password")
            confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password")

            if st.button("Create Account", use_container_width=True):
                if name == "" or signup_email == "" or signup_password == "" or confirm_password == "":
                    st.warning("Please fill all fields")
                elif "@" not in signup_email or "." not in signup_email:
                    st.warning("Please enter valid email")
                elif signup_password != confirm_password:
                    st.error("Passwords do not match ❌")
                elif signup_user(name, signup_email, signup_password):
                    st.success("Account created successfully ✅ Now go to Login tab")
                else:
                    st.error("This email already exists ❌")

    st.stop()

# ================= LOAD DATA =================
if os.path.exists("india_housing_prices.csv"):
    df = pd.read_csv("india_housing_prices.csv")
elif os.path.exists("cleaned_data.pkl"):
    df = joblib.load("cleaned_data.pkl")
else:
    st.error("Dataset not found ❌ Keep india_housing_prices.csv in the same folder")
    st.stop()

# ================= DATA CLEANING =================
df = df.drop_duplicates()

for col in df.columns:
    if df[col].dtype == "object":
        df[col] = df[col].fillna("Unknown")
    else:
        df[col] = df[col].fillna(df[col].median())

required_cols = ["Price_in_Lakhs", "Size_in_SqFt"]

for col in required_cols:
    if col not in df.columns:
        st.error(f"Missing column: {col}")
        st.stop()

if "Price_per_SqFt" not in df.columns:
    df["Price_per_SqFt"] = (df["Price_in_Lakhs"] * 100000) / df["Size_in_SqFt"]

if "Age_of_Property" not in df.columns and "Year_Built" in df.columns:
    df["Age_of_Property"] = 2026 - df["Year_Built"]

df["Future_Price_5_Years"] = df["Price_in_Lakhs"] * 1.35

if "Nearby_Schools" in df.columns and "Nearby_Hospitals" in df.columns:
    df["Good_Investment"] = np.where(
        (df["Price_per_SqFt"] < df["Price_per_SqFt"].median()) &
        (df["Nearby_Schools"] >= df["Nearby_Schools"].median()) &
        (df["Nearby_Hospitals"] >= df["Nearby_Hospitals"].median()),
        "Good Investment",
        "Not Good Investment"
    )
else:
    df["Good_Investment"] = np.where(
        df["Price_per_SqFt"] < df["Price_per_SqFt"].median(),
        "Good Investment",
        "Not Good Investment"
    )

# ================= HEADER =================
st.markdown(f"""
<div class="main-header">
    <h1>🏠 Real Estate Investment Advisor</h1>
    <p class="sub-text">Welcome <b>{st.session_state.user}</b> | Analyze household property price, size, location, amenities and investment potential</p>
</div>
""", unsafe_allow_html=True)

# ================= NAVIGATION =================
nav1, nav2, nav3, nav4, nav5 = st.columns(5)

with nav1:
    if st.button("📊 Dashboard", use_container_width=True):
        st.session_state.page = "Dashboard"

with nav2:
    if st.button("🔮 Prediction", use_container_width=True):
        st.session_state.page = "Prediction"

with nav3:
    if st.button("📈 Visuals", use_container_width=True):
        st.session_state.page = "Visuals"

with nav4:
    if st.button("🔎 Filter", use_container_width=True):
        st.session_state.page = "Filter"

with nav5:
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.login = False
        st.rerun()

# ================= DASHBOARD =================
if st.session_state.page == "Dashboard":

    st.markdown("<div class='section-title'>📊 Executive Dashboard</div>", unsafe_allow_html=True)

    k1, k2, k3, k4, k5 = st.columns(5)

    with k1:
        st.markdown(f"<div class='kpi-card'><p>Total Properties</p><h2>{len(df)}</h2></div>", unsafe_allow_html=True)

    with k2:
        st.markdown(f"<div class='kpi-card'><p>Avg Price</p><h2>₹ {round(df['Price_in_Lakhs'].mean(), 2)} L</h2></div>", unsafe_allow_html=True)

    with k3:
        st.markdown(f"<div class='kpi-card'><p>Avg Size</p><h2>{round(df['Size_in_SqFt'].mean(), 2)}</h2></div>", unsafe_allow_html=True)

    with k4:
        st.markdown(f"<div class='kpi-card'><p>Avg Price/SqFt</p><h2>₹ {round(df['Price_per_SqFt'].mean(), 2)}</h2></div>", unsafe_allow_html=True)

    with k5:
        good_count = df[df["Good_Investment"] == "Good Investment"].shape[0]
        st.markdown(f"<div class='kpi-card'><p>Good Investments</p><h2>{good_count}</h2></div>", unsafe_allow_html=True)

    st.write("")

    c1, c2 = st.columns(2)

    with c1:
        fig = px.histogram(
            df,
            x="Price_in_Lakhs",
            title="Property Price Distribution",
            template="plotly_white"
        )
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig = px.scatter(
            df,
            x="Size_in_SqFt",
            y="Price_in_Lakhs",
            color="Good_Investment",
            title="Property Size vs Price",
            template="plotly_white"
        )
        st.plotly_chart(fig, use_container_width=True)

    c3, c4 = st.columns(2)

    with c3:
        if "City" in df.columns:
            city_df = df.groupby("City")["Price_in_Lakhs"].mean().sort_values(ascending=False).head(10).reset_index()
            fig = px.bar(
                city_df,
                x="City",
                y="Price_in_Lakhs",
                title="Top 10 Cities by Average Price",
                template="plotly_white"
            )
            st.plotly_chart(fig, use_container_width=True)

    with c4:
        investment_df = df["Good_Investment"].value_counts().reset_index()
        investment_df.columns = ["Investment_Status", "Count"]
        fig = px.pie(
            investment_df,
            names="Investment_Status",
            values="Count",
            title="Good Investment vs Not Good Investment"
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("<div class='section-title'>📄 Dataset Preview</div>", unsafe_allow_html=True)
    st.dataframe(df.head(20), use_container_width=True)

# ================= PREDICTION =================
elif st.session_state.page == "Prediction":

    st.markdown("<div class='section-title'>🔮 Investment & Future Price Prediction</div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        price = st.number_input("Property Price in Lakhs", 1.0, 1000.0, 50.0)
        size = st.number_input("Property Size in SqFt", 100.0, 10000.0, 1000.0)

    with c2:
        schools = st.number_input("Nearby Schools", 0, 20, 2)
        hospitals = st.number_input("Nearby Hospitals", 0, 20, 2)

    if st.button("Predict Investment", use_container_width=True):
        price_per_sqft = (price * 100000) / size
        future_price = price * 1.35

        if "Nearby_Schools" in df.columns and "Nearby_Hospitals" in df.columns:
            condition = (
                price_per_sqft < df["Price_per_SqFt"].median()
                and schools >= df["Nearby_Schools"].median()
                and hospitals >= df["Nearby_Hospitals"].median()
            )
        else:
            condition = price_per_sqft < df["Price_per_SqFt"].median()

        r1, r2, r3 = st.columns(3)

        with r1:
            st.metric("Price per SqFt", f"₹ {round(price_per_sqft, 2)}")

        with r2:
            st.metric("Future Price after 5 Years", f"₹ {round(future_price, 2)} L")

        with r3:
            if condition:
                st.success("✅ Good Investment")
            else:
                st.error("❌ Not Good Investment")

# ================= VISUALS =================
elif st.session_state.page == "Visuals":

    st.markdown("<div class='section-title'>📈 Real Estate Visual Analytics</div>", unsafe_allow_html=True)

    chart = st.selectbox(
        "Select Visualization",
        [
            "Average Price by City",
            "Average Price by State",
            "Property Type Count",
            "Price per SqFt by City",
            "BHK Distribution",
            "Furnished Status Analysis",
            "Owner Type Analysis",
            "Availability Status",
            "Nearby Schools vs Price",
            "Nearby Hospitals vs Price",
            "Parking Space vs Price",
            "Age of Property vs Price",
            "Future Price by City",
            "Correlation Heatmap"
        ]
    )

    if chart == "Average Price by City" and "City" in df.columns:
        city_df = df.groupby("City")["Price_in_Lakhs"].mean().sort_values(ascending=False).head(15).reset_index()
        fig = px.bar(city_df, x="City", y="Price_in_Lakhs", title="Average Price by City", template="plotly_white")

    elif chart == "Average Price by State" and "State" in df.columns:
        state_df = df.groupby("State")["Price_in_Lakhs"].mean().sort_values(ascending=False).reset_index()
        fig = px.bar(state_df, x="State", y="Price_in_Lakhs", title="Average Price by State", template="plotly_white")

    elif chart == "Property Type Count" and "Property_Type" in df.columns:
        type_df = df["Property_Type"].value_counts().reset_index()
        type_df.columns = ["Property_Type", "Count"]
        fig = px.bar(type_df, x="Property_Type", y="Count", title="Property Type Distribution", template="plotly_white")

    elif chart == "Price per SqFt by City" and "City" in df.columns:
        sqft_df = df.groupby("City")["Price_per_SqFt"].mean().sort_values(ascending=False).head(15).reset_index()
        fig = px.bar(sqft_df, x="City", y="Price_per_SqFt", title="Price per SqFt by City", template="plotly_white")

    elif chart == "BHK Distribution" and "BHK" in df.columns:
        bhk_df = df["BHK"].value_counts().reset_index()
        bhk_df.columns = ["BHK", "Count"]
        fig = px.bar(bhk_df, x="BHK", y="Count", title="BHK Distribution", template="plotly_white")

    elif chart == "Furnished Status Analysis" and "Furnished_Status" in df.columns:
        furnish_df = df.groupby("Furnished_Status")["Price_in_Lakhs"].mean().reset_index()
        fig = px.bar(furnish_df, x="Furnished_Status", y="Price_in_Lakhs", title="Average Price by Furnished Status", template="plotly_white")

    elif chart == "Owner Type Analysis" and "Owner_Type" in df.columns:
        owner_df = df["Owner_Type"].value_counts().reset_index()
        owner_df.columns = ["Owner_Type", "Count"]
        fig = px.pie(owner_df, names="Owner_Type", values="Count", title="Owner Type Distribution")

    elif chart == "Availability Status" and "Availability_Status" in df.columns:
        avail_df = df["Availability_Status"].value_counts().reset_index()
        avail_df.columns = ["Availability_Status", "Count"]
        fig = px.pie(avail_df, names="Availability_Status", values="Count", title="Availability Status")

    elif chart == "Nearby Schools vs Price" and "Nearby_Schools" in df.columns:
        fig = px.scatter(df, x="Nearby_Schools", y="Price_in_Lakhs", color="Good_Investment", title="Nearby Schools vs Price", template="plotly_white")

    elif chart == "Nearby Hospitals vs Price" and "Nearby_Hospitals" in df.columns:
        fig = px.scatter(df, x="Nearby_Hospitals", y="Price_in_Lakhs", color="Good_Investment", title="Nearby Hospitals vs Price", template="plotly_white")

    elif chart == "Parking Space vs Price" and "Parking_Space" in df.columns:
        fig = px.box(df, x="Parking_Space", y="Price_in_Lakhs", title="Parking Space vs Price", template="plotly_white")

    elif chart == "Age of Property vs Price" and "Age_of_Property" in df.columns:
        fig = px.scatter(df, x="Age_of_Property", y="Price_in_Lakhs", color="Good_Investment", title="Age of Property vs Price", template="plotly_white")

    elif chart == "Future Price by City" and "City" in df.columns:
        future_df = df.groupby("City")["Future_Price_5_Years"].mean().sort_values(ascending=False).head(15).reset_index()
        fig = px.bar(future_df, x="City", y="Future_Price_5_Years", title="Estimated Future Price by City", template="plotly_white")

    elif chart == "Correlation Heatmap":
        numeric_df = df.select_dtypes(include="number")
        fig = px.imshow(numeric_df.corr(), text_auto=True, title="Correlation Heatmap")

    else:
        st.warning("Required column not available in dataset.")
        st.stop()

    st.plotly_chart(fig, use_container_width=True)

# ================= FILTER =================
elif st.session_state.page == "Filter":

    st.markdown("<div class='section-title'>🔎 Property Filter</div>", unsafe_allow_html=True)

    min_price, max_price = st.slider(
        "Select Price Range in Lakhs",
        float(df["Price_in_Lakhs"].min()),
        float(df["Price_in_Lakhs"].max()),
        (float(df["Price_in_Lakhs"].min()), float(df["Price_in_Lakhs"].max()))
    )

    filtered = df[
        (df["Price_in_Lakhs"] >= min_price) &
        (df["Price_in_Lakhs"] <= max_price)
    ]

    if "City" in df.columns:
        city = st.selectbox("Select City", ["All"] + sorted(df["City"].astype(str).unique()))
        if city != "All":
            filtered = filtered[filtered["City"].astype(str) == city]

    if "Property_Type" in df.columns:
        property_type = st.selectbox("Select Property Type", ["All"] + sorted(df["Property_Type"].astype(str).unique()))
        if property_type != "All":
            filtered = filtered[filtered["Property_Type"].astype(str) == property_type]

    if "BHK" in df.columns:
        bhk = st.selectbox("Select BHK", ["All"] + sorted(df["BHK"].astype(str).unique()))
        if bhk != "All":
            filtered = filtered[filtered["BHK"].astype(str) == bhk]

    if "Furnished_Status" in df.columns:
        furnish = st.selectbox("Select Furnished Status", ["All"] + sorted(df["Furnished_Status"].astype(str).unique()))
        if furnish != "All":
            filtered = filtered[filtered["Furnished_Status"].astype(str) == furnish]

    st.success(f"Total Filtered Properties: {filtered.shape[0]}")
    st.dataframe(filtered, use_container_width=True)