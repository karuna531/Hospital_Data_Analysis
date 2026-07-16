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

#replace null
consultation_mean = billing_data["Consultation"].mean()
print(consultation_mean)
billing_data["Consultation"] = billing_data["Consultation"].fillna(consultation_mean)

billing_data["Total"] =billing_data["Total"].fillna( billing_data["Lab"]- billing_data["Discount"] + billing_data["Tax"])
billing_data["PaymentMethod"] = billing_data["PaymentMethod"].fillna(billing_data["PaymentMethod"].mode()[0])

print("missing value", pd.isnull(billing_data).sum())

department_data["Remarks"]= department_data["Remarks"].fillna("No Remarks")
print("Missing Value", pd.isnull(department_data).sum())

diagnosis_data["FollowUp"] =diagnosis_data["FollowUp"].fillna(Not Scheduled)
diagnosis_data["Notes"] = diagnosis_data["Notes"].fillna("Unknown")
print(pd.isnull(diagnosis_data).sum())
print(diagnosis_data["FollowUp"].head(),diagnosis_data["Notes"].head() )