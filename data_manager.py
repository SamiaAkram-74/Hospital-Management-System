"""
Hospital Data Manager 
Handles patient records, appointments, medical records, and billing
"""
import pandas as pd
import numpy as np
import json
import os
from datetime import datetime, timedelta
import traceback

class HospitalDataManager:
    def __init__(self):
        # Get the current directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_dir = os.path.join(current_dir, 'data')
        
        # Create data directory if it doesn't exist
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Define file paths
        self.patients_file = os.path.join(self.data_dir, 'patients.csv')
        self.appointments_file = os.path.join(self.data_dir, 'appointments.csv')
        self.medical_file = os.path.join(self.data_dir, 'medical_records.csv')
        self.billing_file = os.path.join(self.data_dir, 'billing.csv')
        
        # Initialize data files
        self._init_data_files()
        print(f"Data Manager initialized. Files in: {self.data_dir}")
    
    def _init_data_files(self):
        """Initialize CSV files with headers if they don't exist"""
        try:
            # Patients CSV
            if not os.path.exists(self.patients_file):
                patients_df = pd.DataFrame(columns=[
                    'patient_id', 'name', 'age', 'gender', 'contact', 
                    'address', 'email', 'registration_date', 'blood_group'
                ])
                patients_df.to_csv(self.patients_file, index=False)
                print("Created patients.csv")
            
            # Appointments CSV
            if not os.path.exists(self.appointments_file):
                appointments_df = pd.DataFrame(columns=[
                    'appointment_id', 'patient_id', 'patient_name', 'doctor_name',
                    'department', 'appointment_date', 'appointment_time', 'status', 'notes'
                ])
                appointments_df.to_csv(self.appointments_file, index=False)
                print("Created appointments.csv")
            
            # Medical Records CSV
            if not os.path.exists(self.medical_file):
                medical_df = pd.DataFrame(columns=[
                    'record_id', 'patient_id', 'visit_date', 'symptoms', 
                    'diagnosis', 'treatment', 'medication', 'tests', 'notes'
                ])
                medical_df.to_csv(self.medical_file, index=False)
                print("Created medical_records.csv")
            
            # Billing CSV
            if not os.path.exists(self.billing_file):
                billing_df = pd.DataFrame(columns=[
                    'bill_id', 'patient_id', 'patient_name', 'bill_date',
                    'service_type', 'description', 'amount', 'status', 'due_date'
                ])
                billing_df.to_csv(self.billing_file, index=False)
                print("Created billing.csv")
                
        except Exception as e:
            print(f"Error initializing data files: {e}")
            traceback.print_exc()
    
    # ==================== PATIENT MANAGEMENT ====================
    
    def add_patient(self, name, age, gender, contact, address, email="", blood_group=""):
        """Add new patient to CSV"""
        try:
            patients_df = pd.read_csv(self.patients_file)
            
            new_patient = {
                'patient_id': self._generate_id(patients_df, 'patient_id'),
                'name': name,
                'age': int(age),
                'gender': gender,
                'contact': str(contact),
                'address': address,
                'email': email,
                'registration_date': datetime.now().strftime('%Y-%m-%d'),
                'blood_group': blood_group
            }
            
            patients_df = pd.concat([patients_df, pd.DataFrame([new_patient])], ignore_index=True)
            patients_df.to_csv(self.patients_file, index=False)
            print(f"Patient '{name}' registered successfully with ID: {new_patient['patient_id']}")
            return new_patient['patient_id']
        
        except Exception as e:
            print(f"Error adding patient: {e}")
            traceback.print_exc()
            return None
    
    def get_all_patients(self):
        """Get all patients from CSV"""
        try:
            df = pd.read_csv(self.patients_file)
            return df.fillna('')
        except Exception as e:
            print(f"Error reading patients: {e}")
            return pd.DataFrame()
    
    def search_patients(self, search_term):
        """Search patients by name or ID"""
        try:
            patients_df = pd.read_csv(self.patients_file)
            if patients_df.empty:
                return patients_df
            
            mask = (patients_df['name'].astype(str).str.contains(str(search_term), case=False, na=False) | 
                    patients_df['patient_id'].astype(str).str.contains(str(search_term), na=False))
            return patients_df[mask].fillna('')
        except Exception as e:
            print(f"Error searching patients: {e}")
            return pd.DataFrame()
    
    def get_patient_by_id(self, patient_id):
        """Get specific patient by ID"""
        try:
            patients_df = pd.read_csv(self.patients_file)
            result = patients_df[patients_df['patient_id'] == patient_id].fillna('')
            if len(result) == 0:
                print(f"Patient ID {patient_id} not found")
            return result
        except Exception as e:
            print(f"Error getting patient: {e}")
            return pd.DataFrame()
    
    # ==================== APPOINTMENT MANAGEMENT ====================
    
    def schedule_appointment(self, patient_id, doctor_name, department, appointment_date, appointment_time, notes=""):
        """Schedule new appointment"""
        try:
            appointments_df = pd.read_csv(self.appointments_file)
            patients_df = pd.read_csv(self.patients_file)
            
            patient_data = patients_df[patients_df['patient_id'] == patient_id]
            if patient_data.empty:
                print(f"Patient ID {patient_id} not found")
                return None
            
            patient_name = patient_data['name'].iloc[0]
            
            new_appointment = {
                'appointment_id': self._generate_id(appointments_df, 'appointment_id'),
                'patient_id': patient_id,
                'patient_name': patient_name,
                'doctor_name': doctor_name,
                'department': department,
                'appointment_date': appointment_date,
                'appointment_time': appointment_time,
                'status': 'Scheduled',
                'notes': str(notes)  # Ensure notes is string
            }
            
            appointments_df = pd.concat([appointments_df, pd.DataFrame([new_appointment])], ignore_index=True)
            appointments_df.to_csv(self.appointments_file, index=False)
            print(f"Appointment scheduled with Dr. {doctor_name} for {appointment_date} at {appointment_time}")
            return new_appointment['appointment_id']
        
        except Exception as e:
            print(f"Error scheduling appointment: {e}")
            traceback.print_exc()
            return None
    
    def get_all_appointments(self):
        """Get all appointments"""
        try:
            df = pd.read_csv(self.appointments_file)
            return df.fillna('')
        except Exception as e:
            print(f"Error reading appointments: {e}")
            return pd.DataFrame()
    
    def get_appointments_by_date(self, date):
        """Get appointments for specific date"""
        try:
            appointments_df = pd.read_csv(self.appointments_file)
            if appointments_df.empty:
                return appointments_df
            return appointments_df[appointments_df['appointment_date'] == date].fillna('')
        except Exception as e:
            print(f"Error getting appointments by date: {e}")
            return pd.DataFrame()
    
    # ==================== MEDICAL RECORDS METHODS ====================
    
    def add_medical_record(self, patient_id, symptoms, diagnosis, treatment, medication, tests, notes):
        """Add medical record"""
        try:
            medical_df = pd.read_csv(self.medical_file)
            
            new_record = {
                'record_id': self._generate_id(medical_df, 'record_id'),
                'patient_id': patient_id,
                'visit_date': datetime.now().strftime('%Y-%m-%d'),
                'symptoms': str(symptoms),
                'diagnosis': str(diagnosis),
                'treatment': str(treatment),
                'medication': str(medication),
                'tests': str(tests),
                'notes': str(notes)
            }
            
            medical_df = pd.concat([medical_df, pd.DataFrame([new_record])], ignore_index=True)
            medical_df.to_csv(self.medical_file, index=False)
            print(f"Medical record added for patient ID: {patient_id}")
            return new_record['record_id']
        
        except Exception as e:
            print(f"Error adding medical record: {e}")
            traceback.print_exc()
            return None
    
    def get_patient_medical_history(self, patient_id):
        """Get medical history for a patient"""
        try:
            medical_df = pd.read_csv(self.medical_file)
            if medical_df.empty:
                return medical_df
            return medical_df[medical_df['patient_id'] == patient_id].fillna('')
        except Exception as e:
            print(f"Error getting medical history: {e}")
            return pd.DataFrame()
    
    # ==================== BILLING SYSTEM METHODS ====================
    
    def generate_bill(self, patient_id, service_type, description, amount):
        """Generate new bill"""
        try:
            billing_df = pd.read_csv(self.billing_file)
            patients_df = pd.read_csv(self.patients_file)
            
            patient_data = patients_df[patients_df['patient_id'] == patient_id]
            if patient_data.empty:
                print(f"Patient ID {patient_id} not found")
                return None
            
            patient_name = patient_data['name'].iloc[0]
            
            new_bill = {
                'bill_id': self._generate_id(billing_df, 'bill_id'),
                'patient_id': patient_id,
                'patient_name': patient_name,
                'bill_date': datetime.now().strftime('%Y-%m-%d'),
                'service_type': service_type,
                'description': description,
                'amount': float(amount),
                'status': 'Pending',
                'due_date': (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
            }
            
            billing_df = pd.concat([billing_df, pd.DataFrame([new_bill])], ignore_index=True)
            billing_df.to_csv(self.billing_file, index=False)
            print(f"Bill generated for {patient_name}: ${amount} for {service_type}")
            return new_bill['bill_id']
        
        except Exception as e:
            print(f"Error generating bill: {e}")
            traceback.print_exc()
            return None
    
    def get_patient_bills(self, patient_id):
        """Get all bills for a patient"""
        try:
            billing_df = pd.read_csv(self.billing_file)
            if billing_df.empty:
                return billing_df
            return billing_df[billing_df['patient_id'] == patient_id].fillna('')
        except Exception as e:
            print(f"Error getting patient bills: {e}")
            return pd.DataFrame()
    
    def get_all_bills(self):
        """Get all bills"""
        try:
            df = pd.read_csv(self.billing_file)
            return df.fillna('')
        except Exception as e:
            print(f"Error reading bills: {e}")
            return pd.DataFrame()
    
    # ==================== UTILITY METHODS ====================
    
    def _generate_id(self, df, id_column):
        """Generate unique ID"""
        if len(df) == 0:
            return 1001
        try:
            max_id = df[id_column].max()
            if pd.isna(max_id):
                return 1001
            return int(max_id) + 1
        except:
            return 1001
    
    def export_data_to_json(self):
        """Export all data to JSON for frontend use"""
        try:
            # Get all data
            patients_df = self.get_all_patients()
            appointments_df = self.get_all_appointments()
            
            # Read medical and billing files directly
            medical_df = pd.read_csv(self.medical_file)
            billing_df = pd.read_csv(self.billing_file)
            
            # Fill NaN values
            patients_df = patients_df.fillna('')
            appointments_df = appointments_df.fillna('')
            medical_df = medical_df.fillna('')
            billing_df = billing_df.fillna('')
            
            # Convert to dictionaries
            data = {
                'patients': patients_df.to_dict('records'),
                'appointments': appointments_df.to_dict('records'),
                'medical_records': medical_df.to_dict('records'),
                'billing': billing_df.to_dict('records'),
                'export_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # Save to JSON
            json_path = os.path.join(self.data_dir, 'hospital_data.json')
            with open(json_path, 'w') as f:
                json.dump(data, f, indent=2, default=str)
            
            print(f"Data exported to {json_path}")
            return True
            
        except Exception as e:
            print(f"Error exporting data: {e}")
            traceback.print_exc()
            return False
    
    def get_system_stats(self):
        """Get basic system statistics"""
        try:
            stats = {
                'total_patients': len(self.get_all_patients()),
                'total_appointments': len(self.get_all_appointments()),
                'total_medical_records': len(pd.read_csv(self.medical_file)),
                'total_bills': len(self.get_all_bills()),
                'total_revenue': float(self.get_all_bills()['amount'].sum()) if not self.get_all_bills().empty else 0,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            return stats
        except Exception as e:
            print(f"Error getting system stats: {e}")
            return {}

# Test the data manager
if __name__ == "__main__":
    print("Testing HospitalDataManager...")
    dm = HospitalDataManager()
    
    # Test adding a patient
    patient_id = dm.add_patient(
        name="Test Patient",
        age=30,
        gender="Male",
        contact="123-456-7890",
        address="123 Test St",
        email="test@example.com"
    )
    
    if patient_id:
        print(f"Test patient added with ID: {patient_id}")
    
    # Show stats
    stats = dm.get_system_stats()
    print("\nSystem Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")



