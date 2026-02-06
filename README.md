📊 HR Attrition Analytics Platform

An enterprise-grade end-to-end Machine Learning + Analytics system designed to predict employee attrition risk, provide HR insights, and deliver a modern executive dashboard for data-driven workforce decisions.

Built for showcasing Data Analyst • Data Scientist • ML Engineer • AI Engineer skills in a production-ready architecture.

🚀 Live Project Overview

This platform enables HR teams to:

🔮 Predict employee attrition probability

📈 Monitor time-series attrition trends

🔔 Detect high-risk employees

🧑‍💼 Analyze department-level workforce insights

📊 View executive summary dashboards

🔐 Manage users, roles, and authentication

🏗️ System Architecture

Pipeline Flow

Dataset → Feature Engineering → ML Training → Saved Model → Streamlit HR Dashboard → Prediction API → SQLite Logs

Tech Stack Layers

Frontend: Streamlit HR Dashboard (light/dark adaptive UI)

Backend: Python + Scikit-learn ML pipeline

Database: SQLite (user + prediction logs)

Visualization: Plotly interactive charts

Deployment Ready: GitHub / Streamlit Cloud / Docker compatible

🧠 Machine Learning Details Model Capabilities

Attrition classification probability

Handles:

Categorical encoding (OneHotEncoder with unknown handling)

Feature scaling

Missing value safety

Supports real-time HR prediction input

Features Used

Age

Monthly Income

Department

Years at Company

Education

OverTime

Job Role / Job Level

Performance indicators

📊 Dashboard Highlights Executive HR Insights

Workforce distribution

Department attrition comparison

Risk segmentation

KPI metric cards

Advanced Analytics

📈 Time-series attrition trend

🔥 Attrition heatmap

🚨 High-risk employee alerts

👤 Employee profile prediction cards

🔐 Role-Based Access Role Permissions Admin User management, password reset, full monitoring HR Manager Dashboard analytics, prediction insights User Attrition prediction only 📁 Project Structure HR-Attrition-Analytics/ │ ├── app/ │ └── app.py # Streamlit dashboard │ ├── src/ │ ├── generate_dataset.py # Synthetic HR dataset creator │ └── train_model.py # ML training pipeline │ ├── data/ │ └── hr_attrition.csv │ ├── models/ │ ├── hr_attrition_model.pkl │ └── feature_columns.pkl │ ├── database/ │ └── hr.db │ ├── requirements.txt └── README.md

⚙️ Installation & Run 1️⃣ Clone Repository git clone https://github.com/Reenasamuel27/HR-Attrition-Analytics.git cd HR-Attrition-Analytics

2️⃣ Create Virtual Environment python -m venv venv venv\Scripts\activate # Windows

3️⃣ Install Dependencies pip install -r requirements.txt

4️⃣ Generate Dataset & Train Model python src/generate_dataset.py python src/train_model.py

5️⃣ Run HR Dashboard streamlit run app/app.py

📸 Screenshots (Add After Upload)

HR Executive Dashboard

Attrition Prediction Gauge

Risk Heatmap

Admin User Management

(You can drag screenshots into GitHub README later.)

💼 Resume Value

This project demonstrates:

End-to-end ML lifecycle

Feature engineering & model deployment

Interactive analytics dashboard

Role-based enterprise UI

Production-style architecture

Real business HR use-case

Perfect for roles:

Data Analyst • Data Scientist • ML Engineer • AI Engineer

🧑‍💻 Author

Jay Selvam

GitHub: https://github.com/Reenasamuel27

Email: jenisam98896@gmail.com

⭐ Support

If you like this project:

⭐ Star the repository

🍴 Fork it

📢 Share with recruiters

