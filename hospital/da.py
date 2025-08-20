# -------------------------------
# Data Analysis Script (da.py)
# -------------------------------
# Goal: Provide insights on patient care combining patients, doctors, and feedback.

import pandas as pd

# Load processed warehouse data
data = pd.read_csv("data_warehouse/processed_patient_data.csv")

# 1. Number of patients per doctor
patients_per_doctor = data.groupby("doctor_name")["patient_id"].nunique()

# 2. Average feedback score per doctor
if "feedback_score" in data.columns:
    avg_feedback_per_doctor = data.groupby("doctor_name")["feedback_score"].mean()
else:
    avg_feedback_per_doctor = None

# 3. Average feedback score per treatment
if "feedback_score" in data.columns:
    avg_feedback_per_treatment = data.groupby("treatment_id")["feedback_score"].mean()
else:
    avg_feedback_per_treatment = None

# 4. Unique number of patients treated
total_patients = data["patient_id"].nunique()

# Print results
print("\n📊 Data Analysis Report")
print("----------------------------")
print(f"✅ Total unique patients: {total_patients}\n")

print("👨‍⚕️ Patients per doctor:\n", patients_per_doctor, "\n")

if avg_feedback_per_doctor is not None:
    print("⭐ Average feedback score per doctor:\n", avg_feedback_per_doctor, "\n")

if avg_feedback_per_treatment is not None:
    print("💊 Average feedback score per treatment:\n", avg_feedback_per_treatment, "\n")

# Save analysis results
output_file = "data_warehouse/patient_care_analysis.csv"
patients_per_doctor.to_csv(output_file, header=True)
print(f"✅ Analysis results saved to {output_file}")
