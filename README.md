# data_engineering-lab2_hospital
📂 File Organisation

Lab-2/
│
├── hospital/
│   ├── raw_data/                         # Input files
│   │   ├── patients_data_with_doctor.csv
│   │   ├── doctors_info.csv
│   │   └── patient_feedback.json
│   │
│   ├── da.py                             # Business Analyst script (questions + data needs)
│   ├── ml.py                             # Data Engineer script (ETL pipeline)
│   └── README.md                         # Documentation (this file)
│
└── data_warehouse/                       # Output folder (auto-created)
    └── processed_patient_data.csv         # Final processed dataset



🏥 Hospital Dataset – ETL Pipeline

This project integrates patients, doctors, and feedback data to provide a complete view of patient care. The pipeline includes Business Analysis (questions + requirements) and Data Engineering (ETL process).

🔹 Stage 1: Business Analyst Task

Business Question:
How do patients, doctors, and feedback data combine to give a full view of patient care?

Required Data Points:

patient_id

doctor_id

doctor_name

treatment_id

feedback_score

🔹 Stage 2: Data Engineer Task

The ETL pipeline consists of Ingestion → Cleansing → Transformation → Loading.

1️⃣ Ingestion

Read data from multiple sources:

Patients dataset → patients_data_with_doctor.csv

Doctors dataset → doctors_info.csv

Feedback dataset → patient_feedback.json

patients_df = pd.read_csv("hospital/raw_data/patients_data_with_doctor.csv")
doctors_df = pd.read_csv("hospital/raw_data/doctors_info.csv")
feedback_df = pd.read_json("hospital/raw_data/patient_feedback.json", lines=False)

2️⃣ Cleansing

Drop duplicate records from all datasets.

Handle missing feedback scores (replace with 0).

Standardize column names to lowercase.

patients_df = patients_df.drop_duplicates()
doctors_df = doctors_df.drop_duplicates()
feedback_df = feedback_df.drop_duplicates()

feedback_df["feedback_score"] = feedback_df["feedback_score"].fillna(0)

patients_df.columns = [c.strip().lower() for c in patients_df.columns]
doctors_df.columns = [c.strip().lower() for c in doctors_df.columns]
feedback_df.columns = [c.strip().lower() for c in feedback_df.columns]

3️⃣ Transformation

Merge patients with doctors on doctor_id.

Merge with feedback on patient_id and treatment_id.

merged_df = patients_df.merge(doctors_df, on="doctor_id", how="left")

if {"patient_id", "treatment_id"}.issubset(feedback_df.columns):
    merged_df = merged_df.merge(
        feedback_df, on=["patient_id", "treatment_id"], how="left"
    )

4️⃣ Loading

Store the processed dataset into a data warehouse folder.

import os
os.makedirs("data_warehouse", exist_ok=True)

merged_df.to_csv("data_warehouse/processed_patient_data.csv", index=False)


✅ Output File:
data_warehouse/processed_patient_data.csv




🚀 Steps to Run

Navigate to the project folder:

cd Lab-2/hospital


Ensure raw data is present inside hospital/raw_data/.

Run the ETL script:

python ml.py


Check output in:

data_warehouse/processed_patient_data.csv
