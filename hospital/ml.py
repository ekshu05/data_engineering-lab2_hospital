# -------------------------------
# Machine Learning Script (ml.py)
# -------------------------------
# Goal: Predict patient feedback scores based on doctor and treatment data.

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Load processed data
data = pd.read_csv("data_warehouse/processed_patient_data.csv")

# Ensure feedback_score exists
if "feedback_score" not in data.columns:
    raise ValueError("❌ feedback_score column missing in data. Cannot train model.")

# -------------------------------
# 1. Feature Engineering
# -------------------------------
# Convert categorical columns into numeric (dummy encoding)
categorical_cols = ["doctor_name", "doctor_id", "treatment_id"]
data_encoded = pd.get_dummies(data, columns=categorical_cols, drop_first=True)

# Features (X) and Target (y)
X = data_encoded.drop(columns=["feedback_score", "patient_id"])
y = data_encoded["feedback_score"]

# -------------------------------
# 2. Split Data
# -------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -------------------------------
# 3. Train Model
# -------------------------------
model = LinearRegression()
model.fit(X_train, y_train)

# -------------------------------
# 4. Evaluate Model
# -------------------------------
y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("\n🤖 ML Model Evaluation")
print("----------------------------")
print(f"✅ Mean Squared Error: {mse:.2f}")
print(f"✅ R² Score: {r2:.2f}")

# Save model coefficients
coef_output = "data_warehouse/ml_model_coefficients.csv"
pd.DataFrame({"Feature": X.columns, "Coefficient": model.coef_}).to_csv(coef_output, index=False)
print(f"✅ Model coefficients saved to {coef_output}")
