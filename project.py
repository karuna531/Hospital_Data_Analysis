import pandas as pd 
import numpy as np 

#read excel files
appointment_data = pd.read_excel("Data/Appointments.xlsx")
billing_data = pd.read_excel("Data/Billing.xlsx")
department_data = pd.read_excel("Data/Department.xlsx")
diagnosis_data = pd.read_excel("Data/Diagnosis.xlsx")
doctor_data = pd.read_excel("Data/Doctors.xlsx")
insu