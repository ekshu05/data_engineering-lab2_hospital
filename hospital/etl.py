# -------------------------------
# Stage 1: Business Analyst Task
# -------------------------------
# Business Question: How do patients, doctors, and feedback data combine to give a full
# view of patient care? 
# Required data points: patient_id, doctor_id, doctor_name, treatment_id, feedback_score

# -------------------------------
# Stage 2: Data Engineer Task
# -------------------------------

import pandas as pd
import os

# Ensure directory structure
os.makedirs("data_warehouse", exist_ok=True)

# -------------------------------
# 1. Ingestion
# -------------------------------
patients_df = pd.read_csv(r"C:\RVU\Data engineering\lab2\Lab-2\hospital\raw_data\patients_data_with_doctor.csv")   # patient data
doctors_df = pd.read_csv("./raw_data/doctors_info.csv")                    # doctor info
feedback_df = pd.read_json("./raw_data/patient_feedback.json", lines=False) # patient feedback

# -------------------------------
# 2. Cleansing
# -------------------------------
# Drop duplicate records if any
patients_df = patients_df.drop_duplicates()
doctors_df = doctors_df.drop_duplicates()
feedback_df = feedback_df.drop_duplicates()

# Fill missing feedback score with 0 (no feedback)
if "feedback_score" in feedback_df.columns:
    feedback_df["feedback_score"] = feedback_df["feedback_score"].fillna(0)

# Standardize column names (lowercase)
patients_df.columns = [c.strip().lower() for c in patients_df.columns]
doctors_df.columns = [c.strip().lower() for c in doctors_df.columns]
feedback_df.columns = [c.strip().lower() for c in feedback_df.columns]

# -------------------------------
# 3. Transformation
# -------------------------------
# Merge patient with doctor info
merged_df = patients_df.merge(doctors_df, on="doctor_id", how="left")

# Merge with feedback (on patient_id + treatment_id)
if {"patient_id", "treatment_id"}.issubset(feedback_df.columns):
    merged_df = merged_df.merge(
        feedback_df, on=["patient_id", "treatment_id"], how="left"
    )

# -------------------------------
# 4. Load to Warehouse
# -------------------------------
processed_path = "data_warehouse/processed_patient_data.csv"
merged_df.to_csv(processed_path, index=False)

print(f"✅ Processed patient-doctor data saved to {processed_path}")
