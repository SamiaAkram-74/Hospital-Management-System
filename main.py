"""
Hospital Management System - Main Application
"""
import os
import sys
from datetime import datetime

# Add current directory to path to import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_manager import HospitalDataManager
from analytics import HospitalAnalytics
import pandas as pd
import json

def add_sample_data(dm):
    """Add sample data for demonstration"""
    print("\n" + "="*50)
    print("ADDING SAMPLE DATA")
    print("="*50)
    
    sample_patients = [
        {
            "name": "John Smith", 
            "age": 35, 
            "gender": "Male", 
            "contact": "123-456-7890", 
            "address": "123 Main St, City", 
            "email": "john.smith@email.com", 
            "blood_group": "O+"
        },
        {
            "name": "Sarah Johnson", 
            "age": 28, 
            "gender": "Female", 
            "contact": "123-456-7891",
            "address": "456 Oak Ave, Town", 
            "email": "sarah.j@email.com", 
            "blood_group": "A+"
        },
        {
            "name": "Mike Brown", 
            "age": 45, 
            "gender": "Male", 
            "contact": "123-456-7892",
            "address": "789 Pine Rd, Village", 
            "email": "mike.brown@email.com", 
            "blood_group": "B+"
        },
        {
            "name": "Emily Davis", 
            "age": 32, 
            "gender": "Female", 
            "contact": "123-456-7893",
            "address": "321 Elm St, City", 
            "email": "emily.d@email.com", 
            "blood_group": "AB+"
        },
        {
            "name": "Robert Wilson", 
            "age": 60, 
            "gender": "Male", 
            "contact": "123-456-7894",
            "address": "654 Maple Dr, Town", 
            "email": "robert.w@email.com", 
            "blood_group": "O-"
        }
    ]
    
    patient_ids = []
    for patient in sample_patients:
        patient_id = dm.add_patient(**patient)
        if patient_id:
            patient_ids.append(patient_id)
    
    print(f"Added {len(patient_ids)} sample patients")
    
    # Add sample appointments
    if len(patient_ids) >= 4:
        sample_appointments = [
            {
                "patient_id": patient_ids[0], 
                "doctor_name": "Dr. Wilson", 
                "department": "Cardiology", 
                "appointment_date": "2024-01-15", 
                "appointment_time": "10:00 AM",
                "notes": "Regular checkup"
            },
            {
                "patient_id": patient_ids[1], 
                "doctor_name": "Dr. Davis", 
                "department": "Pediatrics", 
                "appointment_date": "2024-01-15", 
                "appointment_time": "11:30 AM",
                "notes": "Child vaccination"
            },
            {
                "patient_id": patient_ids[2], 
                "doctor_name": "Dr. Miller", 
                "department": "Orthopedics", 
                "appointment_date": "2024-01-16", 
                "appointment_time": "02:15 PM",
                "notes": "Knee pain consultation"
            },
            {
                "patient_id": patient_ids[3], 
                "doctor_name": "Dr. Wilson", 
                "department": "Cardiology", 
                "appointment_date": "2024-01-17", 
                "appointment_time": "09:00 AM",
                "notes": "Follow-up appointment"
            }
        ]
        
        for appointment in sample_appointments:
            dm.schedule_appointment(**appointment)
        print("Added sample appointments")
    
    # Add sample medical records
    if len(patient_ids) >= 3:
        sample_medical_records = [
            {
                "patient_id": patient_ids[0], 
                "symptoms": "Chest pain, shortness of breath", 
                "diagnosis": "Hypertension", 
                "treatment": "Medication and lifestyle changes",
                "medication": "Lisinopril 10mg daily", 
                "tests": "ECG, Blood pressure monitoring", 
                "notes": "Follow up in 2 weeks"
            },
            {
                "patient_id": patient_ids[1], 
                "symptoms": "Fever, cough, sore throat", 
                "diagnosis": "Viral infection", 
                "treatment": "Symptomatic treatment",
                "medication": "Paracetamol 500mg", 
                "tests": "Throat swab", 
                "notes": "Rest and hydration recommended"
            },
            {
                "patient_id": patient_ids[2], 
                "symptoms": "Knee pain, swelling", 
                "diagnosis": "Arthritis", 
                "treatment": "Physical therapy",
                "medication": "Ibuprofen 400mg", 
                "tests": "X-ray knee", 
                "notes": "Schedule physical therapy sessions"
            }
        ]
        
        for record in sample_medical_records:
            dm.add_medical_record(**record)
        print("Added sample medical records")
    
    # Add sample bills
    if len(patient_ids) >= 4:
        sample_bills = [
            {
                "patient_id": patient_ids[0], 
                "service_type": "Consultation", 
                "description": "Cardiology Consultation", 
                "amount": 150.00
            },
            {
                "patient_id": patient_ids[0], 
                "service_type": "Tests", 
                "description": "ECG and Blood tests", 
                "amount": 200.00
            },
            {
                "patient_id": patient_ids[1], 
                "service_type": "Consultation", 
                "description": "Pediatrics Consultation", 
                "amount": 120.00
            },
            {
                "patient_id": patient_ids[2], 
                "service_type": "Tests", 
                "description": "X-ray and Diagnosis", 
                "amount": 180.00
            },
            {
                "patient_id": patient_ids[3], 
                "service_type": "Consultation", 
                "description": "Cardiology Follow-up", 
                "amount": 100.00
            }
        ]
        
        for bill in sample_bills:
            dm.generate_bill(**bill)
        print("Added sample bills")
    
    return patient_ids

def get_user_input(prompt, input_type=str, default=None):
    """Helper function to get user input with validation"""
    while True:
        try:
            user_input = input(prompt).strip()
            
            if not user_input and default is not None:
                return default
            
            if not user_input:
                print("This field cannot be empty. Please enter a value.")
                continue
                
            if input_type == int:
                return int(user_input)
            elif input_type == float:
                return float(user_input)
            else:
                return user_input
                
        except ValueError:
            print(f"Invalid input. Please enter a valid {input_type.__name__}.")

def add_patient_interactive(dm):
    """Allow user to add a new patient interactively"""
    print("\n" + "="*50)
    print("ADD NEW PATIENT")
    print("="*50)
    
    print("\nPlease enter patient details:")
    print("-" * 30)
    
    name = get_user_input("Full Name: ")
    age = get_user_input("Age: ", int)
    gender = get_user_input("Gender (Male/Female/Other): ")
    contact = get_user_input("Contact Number: ")
    address = get_user_input("Address: ")
    email = get_user_input("Email (optional): ", default="")
    blood_group = get_user_input("Blood Group (A+, B+, O+, etc.) (optional): ", default="")
    
    patient_id = dm.add_patient(
        name=name,
        age=age,
        gender=gender,
        contact=contact,
        address=address,
        email=email,
        blood_group=blood_group
    )
    
    if patient_id:
        print(f"\nPatient '{name}' added successfully with ID: {patient_id}")
        return patient_id
    else:
        print("Failed to add patient. Please try again.")
        return None

def schedule_appointment_interactive(dm):
    """Allow user to schedule an appointment interactively"""
    print("\n" + "="*50)
    print("SCHEDULE NEW APPOINTMENT")
    print("="*50)
    
    # Show existing patients
    patients = dm.get_all_patients()
    if patients.empty:
        print("No patients found. Please add a patient first.")
        return None
    
    print("\nExisting Patients:")
    print("-" * 40)
    for _, patient in patients.iterrows():
        print(f"ID: {patient['patient_id']} | Name: {patient['name']} | Age: {patient['age']}")
    
    patient_id = get_user_input("\nEnter Patient ID: ", int)
    
    # Check if patient exists
    patient = dm.get_patient_by_id(patient_id)
    if patient.empty:
        print(f"Patient ID {patient_id} not found.")
        return None
    
    print(f"\nScheduling appointment for: {patient.iloc[0]['name']}")
    print("-" * 30)
    
    doctor_name = get_user_input("Doctor's Name: ")
    department = get_user_input("Department: ")
    appointment_date = get_user_input("Appointment Date (YYYY-MM-DD): ")
    appointment_time = get_user_input("Appointment Time (HH:MM AM/PM): ")
    notes = get_user_input("Notes (optional): ", default="")
    
    appointment_id = dm.schedule_appointment(
        patient_id=patient_id,
        doctor_name=doctor_name,
        department=department,
        appointment_date=appointment_date,
        appointment_time=appointment_time,
        notes=notes
    )
    
    if appointment_id:
        print(f"\nAppointment scheduled successfully with ID: {appointment_id}")
        return appointment_id
    else:
        print("Failed to schedule appointment.")
        return None

def add_medical_record_interactive(dm):
    """Allow user to add a medical record interactively"""
    print("\n" + "="*50)
    print("ADD MEDICAL RECORD")
    print("="*50)
    
    # Show existing patients
    patients = dm.get_all_patients()
    if patients.empty:
        print("No patients found. Please add a patient first.")
        return None
    
    print("\nExisting Patients:")
    print("-" * 40)
    for _, patient in patients.iterrows():
        print(f"ID: {patient['patient_id']} | Name: {patient['name']}")
    
    patient_id = get_user_input("\nEnter Patient ID: ", int)
    
    # Check if patient exists
    patient = dm.get_patient_by_id(patient_id)
    if patient.empty:
        print(f"Patient ID {patient_id} not found.")
        return None
    
    print(f"\nAdding medical record for: {patient.iloc[0]['name']}")
    print("-" * 30)
    
    symptoms = get_user_input("Symptoms: ")
    diagnosis = get_user_input("Diagnosis: ")
    treatment = get_user_input("Treatment: ")
    medication = get_user_input("Medication: ")
    tests = get_user_input("Tests conducted: ")
    notes = get_user_input("Additional notes (optional): ", default="")
    
    record_id = dm.add_medical_record(
        patient_id=patient_id,
        symptoms=symptoms,
        diagnosis=diagnosis,
        treatment=treatment,
        medication=medication,
        tests=tests,
        notes=notes
    )
    
    if record_id:
        print(f"\nMedical record added successfully with ID: {record_id}")
        return record_id
    else:
        print("Failed to add medical record.")
        return None

def generate_bill_interactive(dm):
    """Allow user to generate a bill interactively"""
    print("\n" + "="*50)
    print("GENERATE BILL")
    print("="*50)
    
    # Show existing patients
    patients = dm.get_all_patients()
    if patients.empty:
        print("No patients found. Please add a patient first.")
        return None
    
    print("\nExisting Patients:")
    print("-" * 40)
    for _, patient in patients.iterrows():
        print(f"ID: {patient['patient_id']} | Name: {patient['name']}")
    
    patient_id = get_user_input("\nEnter Patient ID: ", int)
    
    # Check if patient exists
    patient = dm.get_patient_by_id(patient_id)
    if patient.empty:
        print(f"Patient ID {patient_id} not found.")
        return None
    
    print(f"\nGenerating bill for: {patient.iloc[0]['name']}")
    print("-" * 30)
    
    service_type = get_user_input("Service Type (e.g., Consultation, Tests, Surgery): ")
    description = get_user_input("Description: ")
    amount = get_user_input("Amount: ", float)
    
    bill_id = dm.generate_bill(
        patient_id=patient_id,
        service_type=service_type,
        description=description,
        amount=amount
    )
    
    if bill_id:
        print(f"\nBill generated successfully with ID: {bill_id}")
        print(f"   Amount: ${amount:.2f}")
        return bill_id
    else:
        print("Failed to generate bill.")
        return None

def search_patient_interactive(dm):
    """Search for patients interactively"""
    print("\n" + "="*50)
    print("SEARCH PATIENT")
    print("="*50)
    
    search_term = get_user_input("Enter name or patient ID to search: ")
    
    results = dm.search_patients(search_term)
    
    if results.empty:
        print(f"No patients found matching '{search_term}'")
        return
    
    print(f"\nFound {len(results)} patient(s):")
    print("-" * 50)
    
    for _, patient in results.iterrows():
        print(f"\nPatient ID: {patient['patient_id']}")
        print(f"Name: {patient['name']}")
        print(f"Age: {patient['age']} | Gender: {patient['gender']}")
        print(f"Contact: {patient['contact']}")
        print(f"Blood Group: {patient['blood_group']}")
        print(f"Registered: {patient['registration_date']}")

def view_system_data(dm):
    """View all system data"""
    print("\n" + "="*50)
    print("SYSTEM DATA VIEW")
    print("="*50)
    
    while True:
        print("\nWhat would you like to view?")
        print("1. All Patients")
        print("2. All Appointments")
        print("3. All Bills")
        print("4. Patient Medical History")
        print("5. Back to Main Menu")
        
        choice = get_user_input("\nEnter your choice (1-5): ", int)
        
        if choice == 1:
            patients = dm.get_all_patients()
            if not patients.empty:
                print("\nALL PATIENTS:")
                print("-" * 60)
                print(patients[['patient_id', 'name', 'age', 'gender', 'contact']].to_string(index=False))
            else:
                print("No patients found.")
                
        elif choice == 2:
            appointments = dm.get_all_appointments()
            if not appointments.empty:
                print("\nALL APPOINTMENTS:")
                print("-" * 70)
                display_cols = ['appointment_id', 'patient_name', 'doctor_name', 
                              'appointment_date', 'appointment_time', 'status']
                print(appointments[display_cols].to_string(index=False))
            else:
                print("No appointments found.")
                
        elif choice == 3:
            bills = dm.get_all_bills()
            if not bills.empty:
                print("\nALL BILLS:")
                print("-" * 70)
                display_cols = ['bill_id', 'patient_name', 'service_type', 
                              'amount', 'status', 'due_date']
                print(bills[display_cols].to_string(index=False))
                
                # Show total
                total = bills['amount'].sum()
                print(f"\nTotal Revenue: ${total:.2f}")
            else:
                print("No bills found.")
                
        elif choice == 4:
            patient_id = get_user_input("Enter Patient ID to view medical history: ", int)
            history = dm.get_patient_medical_history(patient_id)
            
            if not history.empty:
                patient = dm.get_patient_by_id(patient_id)
                patient_name = patient.iloc[0]['name'] if not patient.empty else f"Patient {patient_id}"
                
                print(f"\nMEDICAL HISTORY FOR: {patient_name}")
                print("=" * 60)
                
                for _, record in history.iterrows():
                    print(f"\nVisit Date: {record['visit_date']}")
                    print(f"Symptoms: {record['symptoms']}")
                    print(f"Diagnosis: {record['diagnosis']}")
                    print(f"Treatment: {record['treatment']}")
                    print(f"Medication: {record['medication']}")
                    print(f"Tests: {record['tests']}")
                    if record['notes']:
                        print(f"Notes: {record['notes']}")
                    print("-" * 40)
            else:
                print(f"No medical records found for patient {patient_id}")
                
        elif choice == 5:
            break
        else:
            print("Invalid choice. Please enter 1-5.")

def interactive_main_menu(dm):
    """Interactive main menu for user operations"""
    while True:
        print("\n" + "="*60)
        print("HOSPITAL MANAGEMENT SYSTEM - INTERACTIVE MENU")
        print("="*60)
        
        print("\nMAIN MENU:")
        print("1. Add New Patient")
        print("2. Schedule Appointment")
        print("3. Add Medical Record")
        print("4. Generate Bill")
        print("5. Search Patient")
        print("6. View System Data")
        print("7. Generate Analytics & Reports")
        print("8. View System Statistics")
        print("9. Export Data to JSON")
        print("10. Exit")
        
        choice = get_user_input("\nEnter your choice (1-10): ", int)
        
        if choice == 1:
            add_patient_interactive(dm)
            
        elif choice == 2:
            schedule_appointment_interactive(dm)
            
        elif choice == 3:
            add_medical_record_interactive(dm)
            
        elif choice == 4:
            generate_bill_interactive(dm)
            
        elif choice == 5:
            search_patient_interactive(dm)
            
        elif choice == 6:
            view_system_data(dm)
            
        elif choice == 7:
            print("\n" + "="*50)
            print("GENERATING ANALYTICS AND REPORTS")
            print("="*50)
            
            analytics_response = input("Generate analytics? This will create HTML visualizations (y/n): ").strip().lower()
            if analytics_response == 'y':
                run_analytics(dm)
            else:
                print("Analytics generation skipped.")
                
        elif choice == 8:
            stats = dm.get_system_stats()
            print("\nSYSTEM STATISTICS:")
            print("-" * 30)
            for key, value in stats.items():
                if key == 'total_revenue':
                    print(f"{key.replace('_', ' ').title()}: ${value:.2f}")
                elif key != 'timestamp':
                    print(f"{key.replace('_', ' ').title()}: {value}")
                    
        elif choice == 9:
            if dm.export_data_to_json():
                print("Data exported to JSON successfully")
            else:
                print("Failed to export data")
                
        elif choice == 10:
            print("\nThank you for using Hospital Management System!")
            print("Exiting...")
            break
            
        else:
            print("Invalid choice. Please enter 1-10.")
        
        # Ask if user wants to continue
        if choice != 10:
            continue_response = input("\nReturn to main menu? (y/n): ").strip().lower()
            if continue_response != 'y':
                print("\nThank you for using Hospital Management System!")
                break

def display_system_status(dm):
    """Display system status and sample data"""
    print("\n" + "="*50)
    print("SYSTEM STATUS")
    print("="*50)
    
    stats = dm.get_system_stats()
    print("\nSYSTEM STATISTICS:")
    for key, value in stats.items():
        if key == 'total_revenue':
            print(f"   {key.replace('_', ' ').title()}: ${value:.2f}")
        elif key != 'timestamp':
            print(f"   {key.replace('_', ' ').title()}: {value}")
    
    # Display sample data
    print("\n" + "="*50)
    print("SAMPLE DATA OVERVIEW")
    print("="*50)
    
    # Patients
    patients = dm.get_all_patients()
    if not patients.empty:
        print(f"\nPATIENTS ({len(patients)} total):")
        print("-" * 40)
        display_df = patients[['patient_id', 'name', 'age', 'gender']].head()
        print(display_df.to_string(index=False))
    
    # Appointments
    appointments = dm.get_all_appointments()
    if not appointments.empty:
        print(f"\nAPPOINTMENTS ({len(appointments)} total):")
        print("-" * 40)
        display_df = appointments[['appointment_id', 'patient_name', 'doctor_name', 'appointment_date', 'status']].head()
        print(display_df.to_string(index=False))
    
    # Bills
    bills = dm.get_all_bills()
    if not bills.empty:
        print(f"\nBILLS ({len(bills)} total):")
        print("-" * 40)
        display_df = bills[['bill_id', 'patient_name', 'service_type', 'amount', 'status']].head()
        print(display_df.to_string(index=False))
    
    # Export data to JSON
    print("\n" + "="*50)
    print("EXPORTING DATA")
    print("="*50)
    
    if dm.export_data_to_json():
        print("Data exported to JSON successfully")
    
    return stats

def run_analytics(dm):
    """Run analytics and generate visualizations"""
    print("\n" + "="*50)
    print("STARTING ANALYTICS GENERATION")
    print("="*50)
    
    try:
        analytics = HospitalAnalytics(dm)
        dashboard_data = analytics.generate_all_reports()
        
        # Display analytics summary
        if dashboard_data and 'error' not in dashboard_data:
            print("\nANALYTICS SUMMARY:")
            print("-" * 30)
            
            if 'patient_stats' in dashboard_data:
                ps = dashboard_data['patient_stats']
                if 'error' not in ps:
                    print(f"Patients: {ps.get('total_patients', 0)}")
                    print(f"Avg Age: {ps.get('average_age', 0):.1f}")
            
            if 'appointment_stats' in dashboard_data:
                as_ = dashboard_data['appointment_stats']
                if 'error' not in as_:
                    print(f"Appointments: {as_.get('total_appointments', 0)}")
                    print(f"Top Dept: {as_.get('top_department', 'N/A')}")
            
            if 'financial_stats' in dashboard_data:
                fs = dashboard_data['financial_stats']
                if 'error' not in fs:
                    print(f"Revenue: ${fs.get('total_revenue', 0):.2f}")
                    print(f"Pending: ${fs.get('pending_amount', 0):.2f}")
        
        return True
    except Exception as e:
        print(f"Error running analytics: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main entry point for the hospital management system"""
    print("\n" + "="*60)
    print("HOSPITAL MANAGEMENT SYSTEM")
    print("="*60)
    print("Version: Enhanced with Interactive Features")
    print("="*60)
    
    try:
        # Initialize data manager
        dm = HospitalDataManager()
        
        # Check if we have existing data
        existing_patients = dm.get_all_patients()
        
        print("\nSYSTEM INITIALIZATION")
        print("-" * 30)
        
        if len(existing_patients) == 0:
            print("No existing data found.")
            response = input("Would you like to add sample data? (y/n): ").strip().lower()
            if response == 'y':
                print("\nAdding sample data...")
                patient_ids = add_sample_data(dm)
            else:
                print("Starting with empty database.")
        else:
            print(f"Found existing data with {len(existing_patients)} patients.")
        
        # Display system status
        print("\n" + "="*50)
        display_response = input("Display system status? (y/n): ").strip().lower()
        if display_response == 'y':
            stats = display_system_status(dm)
        
        # Ask about mode selection
        print("\n" + "="*50)
        print("SELECT OPERATION MODE")
        print("="*50)
        print("\n1. Interactive Mode (Add/view data manually)")
        print("2. Quick Mode (Generate analytics and exit)")
        print("3. Exit")
        
        mode_choice = get_user_input("\nEnter your choice (1-3): ", int)
        
        if mode_choice == 1:
            # Interactive mode
            print("\n" + "="*60)
            print("ENTERING INTERACTIVE MODE")
            print("="*60)
            print("\nYou can now:")
            print("• Add new patients, appointments, medical records, bills")
            print("• Search for patients")
            print("• View all system data")
            print("• Generate analytics reports")
            
            interactive_main_menu(dm)
            
        elif mode_choice == 2:
            # Quick mode - generate analytics
            print("\n" + "="*50)
            print("QUICK MODE - GENERATING ANALYTICS")
            print("="*50)
            
            analytics_response = input("Generate analytics and visualizations? (y/n): ").strip().lower()
            if analytics_response == 'y':
                run_analytics(dm)
                
                print("\n" + "="*60)
                print("ANALYTICS GENERATION COMPLETE!")
                print("="*60)
                print("\nFiles created:")
                print(f"   Data files: {os.path.abspath(dm.data_dir)}/")
                print(f"   Visualizations: {os.path.abspath('visualizations/')}/")
                print("\nNext steps:")
                print("   1. Open HTML files in the 'visualizations/' folder")
                print("   2. Check 'data/hospital_data.json' for complete dataset")
                print("   3. Run the system again to add more data")
        
        elif mode_choice == 3:
            print("\nThank you for using Hospital Management System!")
            print("Exiting...")
        
        else:
            print("Invalid choice. Exiting...")
        
        print("\n" + "="*60)
        print("SYSTEM SHUTDOWN COMPLETE!")
        print("="*60)
        
    except Exception as e:
        print(f"\nError in main execution: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    # Run the main function
    exit_code = main()
    
    # Keep the console open if running from executable
    if exit_code != 0:
        input("\nPress Enter to exit...")
    sys.exit(exit_code)