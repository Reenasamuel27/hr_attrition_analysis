import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import joblib
import plotly.express as px
import plotly.graph_objects as go
import hashlib
import os
from datetime import datetime

# =====================================================
# PATH SAFE LOADING (FIXES YOUR ERROR FOREVER)
# =====================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(BASE_DIR, "models", "hr_attrition_model.pkl")
FEATURES_PATH = os.path.join(BASE_DIR, "models", "feature_columns.pkl")
DB_PATH = os.path.join(BASE_DIR, "database", "hr.db")

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"❌ Model not found: {MODEL_PATH}")

model = joblib.load(MODEL_PATH)
features = joblib.load(FEATURES_PATH)

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="HR Attrition Analytics",
    page_icon="👤",
    layout="wide"
)

# =====================================================
# DATABASE
# =====================================================
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS users(
    username TEXT PRIMARY KEY,
    password TEXT,
    role TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS predictions(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user TEXT,
    department TEXT,
    risk REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS password_reset_requests(
    username TEXT PRIMARY KEY,
    requested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()

# =====================================================
# HELPERS
# =====================================================
def hash_pw(p):
    return hashlib.sha256(p.encode()).hexdigest()

def add_user(u, p, role="employee"):
    c.execute(
        "INSERT OR IGNORE INTO users VALUES (?,?,?)",
        (u, hash_pw(p), role)
    )
    conn.commit()

def login(u, p):
    c.execute(
        "SELECT role FROM users WHERE username=? AND password=?",
        (u, hash_pw(p))
    )
    r = c.fetchone()
    return r[0] if r else None

def log_prediction(user, dept, risk):
    c.execute(
        "INSERT INTO predictions(user, department, risk) VALUES (?,?,?)",
        (user, dept, float(risk))
    )
    conn.commit()

def get_logs():
    return pd.read_sql("SELECT * FROM predictions", conn)

def request_password_reset(u):
    c.execute(
        "INSERT OR IGNORE INTO password_reset_requests VALUES (?,CURRENT_TIMESTAMP)",
        (u,)
    )
    conn.commit()

def get_reset_requests():
    return pd.read_sql("SELECT * FROM password_reset_requests", conn)

def reset_password(u, new_pw):
    c.execute(
        "UPDATE users SET password=? WHERE username=?",
        (hash_pw(new_pw), u)
    )
    c.execute(
        "DELETE FROM password_reset_requests WHERE username=?",
        (u,)
    )
    conn.commit()

# Default admin
add_user("admin", "admin123", "admin")

# =====================================================
# SESSION
# =====================================================
if "user" not in st.session_state:
    st.session_state.user = None
if "role" not in st.session_state:
    st.session_state.role = None

# =====================================================
# LOGIN PAGE
# =====================================================
if not st.session_state.user:
    st.title("👥 HR Attrition Analytics Platform")

    t1, t2, t3 = st.tabs(["🔐 Login", "➕ Register", "🔁 Reset Password"])

    with t1:
        u = st.text_input("Username", key="login_u")
        p = st.text_input("Password", type="password", key="login_p")
        if st.button("Login"):
            role = login(u, p)
            if role:
                st.session_state.user = u
                st.session_state.role = role
                st.rerun()
            else:
                st.error("Invalid credentials")

    with t2:
        nu = st.text_input("New Username", key="reg_u")
        npw = st.text_input("Password", type="password", key="reg_p")
        if st.button("Create Account"):
            add_user(nu, npw)
            st.success("Account created")

    with t3:
        fu = st.text_input("Username", key="reset_u")
        if st.button("Request Reset"):
            request_password_reset(fu)
            st.success("Reset request sent to HR admin")

    st.stop()

# =====================================================
# SIDEBAR (NEW HR STYLE)
# =====================================================
st.sidebar.markdown("## 👤 HR Control Panel")
st.sidebar.info(f"**User:** {st.session_state.user}")
st.sidebar.info(f"**Role:** {st.session_state.role}")

if st.sidebar.button("Logout"):
    st.session_state.user = None
    st.session_state.role = None
    st.rerun()

page = st.sidebar.radio(
    "Navigate",
    ["Dashboard", "Predict Attrition", "Insights", "Alerts", "Admin"]
)

df = get_logs()

# =====================================================
# DASHBOARD
# =====================================================
if page == "Dashboard":
    st.markdown("## 📊 Executive Summary")

    col1, col2, col3, col4 = st.columns(4)

    avg_risk = df["risk"].mean() if not df.empty else 0
    high_risk = (df["risk"] > 0.7).sum() if not df.empty else 0

    col1.metric("Total Employees", len(df))
    col2.metric("Avg Attrition Risk", f"{avg_risk:.2f}")
    col3.metric("High Risk Employees", high_risk)
    col4.metric("Departments", df["department"].nunique() if not df.empty else 0)

    if not df.empty:
        st.divider()

        st.markdown("### 📉 Attrition Trend Over Time")
        trend = df.copy()
        trend["created_at"] = pd.to_datetime(trend["created_at"])
        trend = trend.groupby(trend["created_at"].dt.date)["risk"].mean().reset_index()

        fig = px.line(trend, x="created_at", y="risk", markers=True)
        st.plotly_chart(fig, use_container_width=True)

# =====================================================
# PREDICT ATTRITION (FINAL FIXED VERSION)
# =====================================================
if page == "Predict Attrition":
    st.markdown("## 👤 Employee Attrition Prediction")

    c1, c2, c3 = st.columns(3)
    age = c1.slider("Age", 18, 60, 30)
    income = c2.slider("Monthly Income", 1000, 20000, 6000)
    years = c3.slider("Years at Company", 0, 40, 5)

    c4, c5, c6 = st.columns(3)
    job_level = c4.selectbox("Job Level", [1, 2, 3, 4, 5])
    work_life = c5.selectbox("Work Life Balance", [1, 2, 3, 4])
    job_satisfaction = c6.selectbox("Job Satisfaction", [1, 2, 3, 4])

    c7, c8 = st.columns(2)
    education = c7.selectbox(
        "Education Level",
        ["Below College", "College", "Bachelor", "Master", "Doctor"]
    )

    overtime_label = c8.selectbox(
        "Over Time",
        ["Yes", "No"]
    )

    dept = st.selectbox(
        "Department",
        ["HR", "IT", "Sales", "Finance", "Operations"]
    )

    role = st.selectbox(
        "Job Role",
        ["Manager", "Engineer", "Executive", "Analyst", "Sales Rep"]
    )

    if st.button("🔮 Predict Attrition Risk"):

        # ===============================
        # ✅ MATCH TRAINING SCHEMA EXACTLY
        # ===============================
        input_df = pd.DataFrame([{
            "Age": float(age),
            "MonthlyIncome": float(income),
            "YearsAtCompany": float(years),
            "JobLevel": float(job_level),
            "WorkLifeBalance": float(work_life),
            "JobSatisfaction": float(job_satisfaction),

            # 🔥 FIX: OverTime numeric
            "OverTime": float(1 if overtime_label == "Yes" else 0),

            # Categorical (as trained)
            "Education": education,
            "Department": dept,
            "JobRole": role
        }])

        # ===============================
        # 🎯 PREDICTION
        # ===============================
        risk = float(model.predict_proba(input_df)[0, 1])

        log_prediction(
            st.session_state.user,
            dept,
            risk
        )

        # ===============================
        # 📊 GAUGE VISUAL
        # ===============================
        fig = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=risk * 100,
                number={"suffix": "%"},
                title={"text": "Attrition Risk"},
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": "#ef4444"},
                    "steps": [
                        {"range": [0, 30], "color": "#22c55e"},
                        {"range": [30, 60], "color": "#facc15"},
                        {"range": [60, 100], "color": "#ef4444"},
                    ],
                },
            )
        )

        st.plotly_chart(fig, use_container_width=True)

        if risk >= 0.6:
            st.error("🚨 High attrition risk — immediate HR action recommended.")
        elif risk >= 0.3:
            st.warning("⚠️ Moderate attrition risk — monitor engagement.")
        else:
            st.success("✅ Low attrition risk — employee appears stable.")


# =====================================================
# INSIGHTS
# =====================================================
if page == "Insights" and not df.empty:
    st.markdown("## 📈 Workforce Insights")

    heat = df.pivot_table(
        index="department",
        values="risk",
        aggfunc="mean"
    ).reset_index()

    fig = px.imshow(
        heat.set_index("department"),
        text_auto=True,
        color_continuous_scale="Reds",
        title="🔥 Attrition Heatmap by Department"
    )
    st.plotly_chart(fig, use_container_width=True)

# =====================================================
# ALERTS
# =====================================================
if page == "Alerts":
    st.markdown("## 🔔 High Risk Employee Alerts")

    alerts = df[df["risk"] > 0.7]
    if alerts.empty:
        st.success("No high-risk employees 🎉")
    else:
        st.dataframe(alerts, use_container_width=True)

# =====================================================
# ADMIN
# =====================================================
if page == "Admin":
    if st.session_state.role != "admin":
        st.error("Admin only")
        st.stop()

    st.markdown("## 🛠 HR Admin Panel")

    t1, t2 = st.tabs(["👥 Users", "🔐 Reset Requests"])

    with t1:
        users = pd.read_sql("SELECT username, role FROM users", conn)
        st.dataframe(users, use_container_width=True)

        nu = st.text_input("Username", key="admin_u")
        npw = st.text_input("Password", type="password", key="admin_p")
        nr = st.selectbox("Role", ["employee", "hr_manager", "admin"])
        if st.button("Create User"):
            add_user(nu, npw, nr)
            st.success("User created")
            st.rerun()

    with t2:
        reqs = get_reset_requests()
        for _, r in reqs.iterrows():
            new_pw = st.text_input(
                f"New password for {r['username']}",
                type="password",
                key=r['username']
            )
            if st.button(f"Reset {r['username']}"):
                reset_password(r["username"], new_pw)
                st.success("Password reset")
                st.rerun()