import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

df = pd.read_csv("data/hr_attrition_60000.csv")

X = df.drop("Attrition", axis=1)
y = df["Attrition"]

cat_cols = ["Department", "JobRole", "Education"]
num_cols = [c for c in X.columns if c not in cat_cols]

preprocessor = ColumnTransformer([
    ("num", StandardScaler(), num_cols),
    ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols)
])

model = RandomForestClassifier(
    n_estimators=200,
    max_depth=10,
    random_state=42
)

pipeline = Pipeline([
    ("prep", preprocessor),
    ("model", model)
])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

pipeline.fit(X_train, y_train)

preds = pipeline.predict(X_test)
print(classification_report(y_test, preds))

joblib.dump(pipeline, "models/hr_attrition_model.pkl")
joblib.dump(X.columns.tolist(), "models/feature_columns.pkl")

print("✅ Model trained & saved")
