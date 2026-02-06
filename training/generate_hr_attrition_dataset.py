import pandas as pd
import numpy as np

np.random.seed(42)
N = 60000

departments = ["IT", "HR", "Finance", "Sales", "Operations"]
job_roles = ["Executive", "Manager", "Senior", "Junior"]
education = ["High School", "Bachelor", "Master", "PhD"]

df = pd.DataFrame({
    "Age": np.random.randint(21, 60, N),
    "Department": np.random.choice(departments, N),
    "JobRole": np.random.choice(job_roles, N),
    "Education": np.random.choice(education, N),
    "MonthlyIncome": np.random.randint(20000, 200000, N),
    "YearsAtCompany": np.random.randint(0, 20, N),
    "JobSatisfaction": np.random.randint(1, 5, N),
    "WorkLifeBalance": np.random.randint(1, 5, N),
    "OverTime": np.random.choice([0, 1], N),
})

# -------- ATTRITION LOGIC (REALISTIC) ----------
risk = (
    (df["JobSatisfaction"] <= 2).astype(int) * 0.3 +
    (df["WorkLifeBalance"] <= 2).astype(int) * 0.25 +
    (df["OverTime"] == 1).astype(int) * 0.2 +
    (df["YearsAtCompany"] < 2).astype(int) * 0.15 +
    (df["MonthlyIncome"] < 40000).astype(int) * 0.2
)

prob = np.clip(risk + np.random.normal(0, 0.05, N), 0, 1)
df["Attrition"] = (prob > 0.5).astype(int)

df.to_csv("data/hr_attrition_60000.csv", index=False)
print("✅ Dataset generated: 60,000 rows")
