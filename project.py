import pandas as pd 
import numpy as np 

#read excel files
appointment_data = pd.read_excel("Data/Appointments.xlsx")
billing_data = pd.read_excel("Data/Billing.xlsx")
department_data = pd.read_excel("Data/Department.xlsx")
diagnosis_data = pd.read_excel("Data/Diagnosis.xlsx")
doctor_data = pd.read_excel("Data/Doctors.xlsx")
insurance_data= pd.read_excel("Data/Insurance.xlsx")
patient_data = pd.read_excel("Data/Patients.xlsx")
pharmacy_data = pd.read_excel("Data/Pharmacy.xlsx")
visit_data = pd.read_excel("Data/Visits.xlsx")

# view excel details
# print( appointment_data.head())
# print( appointment_data.info())
# print( appointment_data.describe())
print(appointment_data.shape)
print(appointment_data.columns)
print(billing_data.shape)
print(billing_data.columns)
print(department_data.columns)
print(diagnosis_data.columns)
print(doctor_data.columns)
print(insurance_data.columns)
print(patient_data.columns)
print(pharmacy_data.columns)
print(visit_data.columns)

#check data Null,duplicate, Infinite, and wrong data
appointment_null = pd.isnull(appointment_data).sum()
print("Null in Appointment", appointment_null)
print("Null in Billing", pd.isnull(billing_data).sum())
print("Null in Department", pd.isnull(department_data).sum())
print("Null in Diagnosis", pd.isnull(diagnosis_data).sum())
print("Null in Doctor", pd.isnull(doctor_data).sum())
print("Null in insurance", pd.isnull(insurance_data).sum())
print("Null in patient", pd.isnull(patient_data).sum())
print("Null in Pharmacy", pd.isnull(pharmacy_data).sum())
print("Null in visit", pd.isnull(visit_data).sum())

Appointment_duplicate = appointment_data.duplicated().sum()
print("Appointment Duplicates",Appointment_duplicate )
print("Billing Duplicate", billing_data.duplicated().sum())
print("Department Duplicates",department_data.duplicated().sum())
print("Diagnosis Duplicates",diagnosis_data.duplicated().sum())
print("Doctor Duplicates", doctor_data.duplicated().sum())
print("Insurance Duplicates",insurance_data.duplicated().sum())
print("patient Duplicates",patient_data.duplicated().sum())
print("Pharmacy Duplicates", pharmacy_data.duplicated().sum())
print("Visit Duplicates",visit_data.duplicated().sum())

#remove duplicates
appointment = appointment_data.drop_duplicates(subset=["AppointmentID"], keep = "first")
diagnosis = diagnosis_data.drop_duplicates(subset=["DiagnosisID"], keep = "first")
doctor = doctor_data.drop_duplicates(subset=["DoctorID"], keep ="first")
pharmacy = pharmacy_data.drop_duplicates(subset=["SaleID"], keep = "first")
department = department_data.drop_duplicates(subset=["Department"], keep="first")
insurance = insurance_data.drop_duplicates(subset=["InsuranceID"], keep="first")
billing = billing_data.sort_values("BillID").drop_duplicates(subset=["VisitID"], keep="first")
insurance = insurance.sort_values("InsuranceID").drop_duplicates(
    subset="PatientID", keep="first"
)

diagnosis = diagnosis.sort_values("DiagnosisID").drop_duplicates(
    subset="PatientID", keep="first"
)

pharmacy = pharmacy.sort_values("SaleID").drop_duplicates(
    subset="PatientID", keep="first"
)


# standardarize 
gender_map ={
    'm': 'Male', 'M': 'Male', 'Mal':'Male', 'male': 'Male', 'Male':'Male', 
    'f': 'Female', 'fmale': 'Female', 'female':'Female', 'femal':'Female', 'FeMale':'FeMale', 'F': 'Female'
}
patient_data["Gender"] = patient_data["Gender"].astype(str).str.strip().replace(gender_map)
print(department_data['Department'].unique())
department_map ={
    'endo': 'Endo', 'end':'Endo', 'edo':'Endo', 'Endo': 'Endo',
    'pedo': 'Pedo', 'ped': 'Pedo', 'pedoo': 'Pedo', 'pdo': 'Pedo', 'Pedo': 'Pedo',
    'ortho': 'Ortho', 'orth': 'Ortho', 'ort': 'Ortho', 'Ortho': 'Ortho',
    'perio': 'Perio', 'Perio': 'Perio', 'Pero': 'Perio',
    'Prostho': 'Prostho', 'prostho': 'Prostho', 
    'dental': 'Dental', 'Dntal': 'Dental', 'den': 'Dental'
}
department_data["Department"] = department_data["Department"].astype(str).str.strip().replace(department_map)

# remove leading and trailing space
dataset = [
    appointment,
    billing,
    department,
    diagnosis,
    doctor,
    insurance,
    patient_data,
    pharmacy,
    visit_data
]
for df in dataset:
    obj = df.select_dtypes(include='string').columns
    df[obj]=df[obj].apply(lambda x: x.str.strip())
print("leading and trailing space is removed")

#Convert dates into datetime format. 
joining_date = pd.to_datetime( doctor["JoiningDate"], errors='coerce')
print(joining_date.min())

# converting Bill columns to numeric
billing_data["Total"] =pd.to_numeric(billing["Total"], errors="coerce")

#finding invalid age
invalid_age = (patient_data["Age"] < 0) | (patient_data["Age"] > 150)
print("invalid_age", invalid_age.sum())
patient_data["Age"] = patient_data.loc[invalid_age, "Age"] = pd.NA
# Remove negative bills
# negative_bill = billing_data["Total"] < 0
# print("Negative Bill", negative_bill.sum())
# billing_data["Total"] = billing_data.loc[negative_bill, "Total"] = pd.NA

bill_amount_cols = ['Consultation', 'Procedure', 'Lab', 'Discount', 'Tax', 'Total']

neg_mask = (billing[bill_amount_cols] < 0).any(axis=1)
neg_count = neg_mask.sum()

billing_data = billing.loc[~neg_mask].reset_index(drop=True)

print(f"Removed {neg_count} rows containing a negative bill amount.")


#replace null
consultation_mean = billing["Consultation"].mean()
billing["Consultation"] = billing["Consultation"].fillna(consultation_mean)

billing["Total"] =billing["Total"].fillna( billing_data["Lab"]- billing_data["Discount"] + billing_data["Tax"])
billing["PaymentMethod"] = billing["PaymentMethod"].fillna(billing["PaymentMethod"].mode()[0])


department["Remarks"]= department["Remarks"].fillna("No Remarks")

diagnosis["FollowUp"] =diagnosis["FollowUp"].fillna("Not Scheduled")
diagnosis["Notes"] = diagnosis["Notes"].fillna("Unknown")
insurance["Provider"] = insurance["Provider"].fillna( insurance_data["Provider"].mode()[0])
patient_data["BloodGroup"]= patient_data["BloodGroup"].fillna("unidentified")
# mode = patient_data["Insurance"].mode()[0]
patient_data["Insurance"]=patient_data["Insurance"].fillna("Unknown")
patient_data["Age"]=patient_data["Age"].fillna(patient_data["Age"].median())
patient_data["Gender"] = patient_data["Gender"].fillna("unidentified")
patient_data["District"] = patient_data["District"].fillna("Not Mentioned")
pharmacy["PaymentMethod"]= pharmacy["PaymentMethod"].fillna(pharmacy_data["PaymentMethod"].mode()[0])

# merging all excel file to master dataset
master = visit_data.copy()
print("Patients:", master.shape)
master = master.merge(patient_data, on = "PatientID", how="left", suffixes=("","_patient"))
print("Patients:", master.shape)
master = master.merge(appointment, on="AppointmentID", how= "left", suffixes=("","_appointment"))
print("Patients:", master.shape)
master = master.merge(doctor, on="DoctorID", how="left", suffixes=("", "_doctor"))
print("Doctor:", master.shape)
master = master.merge(insurance, on="PatientID", how="left", suffixes=("", "_insurance"))
print("insurance:", master.shape)
master = master.merge(department, on="Department", how="left", suffixes=("", "_department"))
master = master.merge(diagnosis, on="PatientID", how="left", suffixes=("", "_diagnosis"))
master = master.merge(pharmacy, on="PatientID", how="left", suffixes=("", "_pharmacy"))
master = master.merge(billing, on="VisitID", how="left", suffixes=("", "_billing"))
print("Billing:", master.shape)
print("Patients:", master.shape)

master.to_excel("Output/hospital_cleaned_data.xlsx", index=False)
master.to_csv("Output/hospital_cleaned_data.csv", index=False)
print(master.head())
#total patients
total_patients = master["PatientID"].count()
print("Total No of Patients:", total_patients)
#no of male vs female
male_vs_female = master.groupby("Gender").size()
print(male_vs_female)
#Unique patients.
unique_patients = master["PatientID"].nunique()
print("Unique Patients:", unique_patients) 

#Patients by district. 
patient_by_district = master.groupby("District")["PatientID"].size()
print("patient_by_district", patient_by_district)

# Patients by age group.
age_group = master["Age"] 