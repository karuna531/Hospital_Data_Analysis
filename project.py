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


# standardarize 
gender_map ={
    'm': 'Male', 'M': 'Male', 'Mal':'Male', 'male': 'Male', 'Male':'Male', 
    'f': 'Female', 'fmale': 'Female', 'female':'Female', 'femal':'Female', 'FeMale':'FeMale'
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
    appointment_data,
    billing_data,
    department_data,
    diagnosis_data,
    doctor_data,
    insurance_data,
    patient_data,
    pharmacy_data,
    visit_data
]
for df in dataset:
    obj = df.select_dtypes(include='string').columns
    df[obj]=df[obj].apply(lambda x: x.str.strip())
print("leading and trailing space is removed")

#Convert dates into datetime format. 
joining_date = pd.to_datetime( doctor_data["JoiningDate"], errors='coerce')
print(joining_date.min())
#replace null
consultation_mean = billing_data["Consultation"].mean()
billing_data["Consultation"] = billing_data["Consultation"].fillna(consultation_mean)

billing_data["Total"] =billing_data["Total"].fillna( billing_data["Lab"]- billing_data["Discount"] + billing_data["Tax"])
billing_data["PaymentMethod"] = billing_data["PaymentMethod"].fillna(billing_data["PaymentMethod"].mode()[0])


department_data["Remarks"]= department_data["Remarks"].fillna("No Remarks")

diagnosis_data["FollowUp"] =diagnosis_data["FollowUp"].fillna("Not Scheduled")
diagnosis_data["Notes"] = diagnosis_data["Notes"].fillna("Unknown")
insurance_data["Provider"] = insurance_data["Provider"].fillna( insurance_data["Provider"].mode()[0])
patient_data["BloodGroup"]= patient_data["BloodGroup"].fillna("unidentified")
# mode = patient_data["Insurance"].mode()[0]
patient_data["Insurance"]=patient_data["Insurance"].fillna("Unknown")
patient_data["Age"]=patient_data["Age"].fillna(patient_data["Age"].mean())
patient_data["Gender"] = patient_data["Gender"].fillna("unidentified")
patient_data["District"] = patient_data["District"].fillna("Not Mentioned")
pharmacy_data["PaymentMethod"]= pharmacy_data["PaymentMethod"].fillna(pharmacy_data["PaymentMethod"].mode()[0])


