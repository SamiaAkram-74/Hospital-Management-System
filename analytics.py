"""
Hospital Analytics System 
Generates visualizations and analytics reports
"""
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import json
import os
from datetime import datetime
import traceback

class HospitalAnalytics:
    def __init__(self, data_manager):
        self.dm = data_manager
        
        # Method 1: Using data_dir to find project folder
        project_dir = os.path.dirname(self.dm.data_dir)  
        
        # Method 2: Or use current file location
        # current_dir = os.path.dirname(os.path.abspath(__file__))
        # project_dir = current_dir
        
        self.viz_dir = os.path.join(project_dir, 'visualizations')
        
        # Create visualizations directory
        os.makedirs(self.viz_dir, exist_ok=True)
        print(f"Analytics initialized. Visualizations will be saved to: {self.viz_dir}")
        print(f"    Visualizations path: {os.path.abspath(self.viz_dir)}")
    
    def _convert_numpy_types(self, obj):
        """Convert NumPy types to native Python types for JSON serialization"""
        if isinstance(obj, (np.integer, np.int64, np.int32)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float64, np.float32)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, dict):
            return {key: self._convert_numpy_types(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [self._convert_numpy_types(item) for item in obj]
        elif pd.isna(obj):
            return None
        else:
            return obj
    
    def generate_patient_statistics(self):
        """Generate patient demographics statistics and charts"""
        print("Generating patient statistics...")
        
        try:
            patients_df = self.dm.get_all_patients()
            
            if patients_df.empty or len(patients_df) == 0:
                print("No patient data available")
                return {"error": "No patient data available", "total_patients": 0}
            
            # 1. Gender Distribution Pie Chart
            gender_counts = patients_df['gender'].value_counts()
            if len(gender_counts) > 0:
                fig1 = px.pie(
                    values=gender_counts.values, 
                    names=gender_counts.index,
                    title='Patient Gender Distribution',
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                fig1.update_traces(textposition='inside', textinfo='percent+label')
                fig1.write_html(os.path.join(self.viz_dir, 'gender_distribution.html'))
                print(f"Generated {os.path.join(self.viz_dir, 'gender_distribution.html')}")
            
            # 2. Age Distribution Histogram
            if 'age' in patients_df.columns:
                fig2 = px.histogram(
                    patients_df, 
                    x='age', 
                    nbins=10,
                    title='Patient Age Distribution',
                    labels={'age': 'Age', 'count': 'Number of Patients'},
                    color_discrete_sequence=['#1f77b4']
                )
                fig2.update_layout(bargap=0.1)
                fig2.write_html(os.path.join(self.viz_dir, 'age_distribution.html'))
                print(f"Generated {os.path.join(self.viz_dir, 'age_distribution.html')}")
            
            # 3. Blood Group Distribution
            if 'blood_group' in patients_df.columns:
                blood_group_counts = patients_df['blood_group'].value_counts()
                if len(blood_group_counts) > 0:
                    fig3 = px.bar(
                        x=blood_group_counts.index, 
                        y=blood_group_counts.values,
                        title='Blood Group Distribution',
                        labels={'x': 'Blood Group', 'y': 'Number of Patients'},
                        color=blood_group_counts.values,
                        color_continuous_scale='Viridis'
                    )
                    fig3.write_html(os.path.join(self.viz_dir, 'blood_group_distribution.html'))
                    print(f"Generated {os.path.join(self.viz_dir, 'blood_group_distribution.html')}")
            
            # Calculate statistics
            stats = {
                'total_patients': len(patients_df),
                'average_age': float(patients_df['age'].mean()) if 'age' in patients_df.columns and not patients_df['age'].isna().all() else 0,
                'min_age': int(patients_df['age'].min()) if 'age' in patients_df.columns else 0,
                'max_age': int(patients_df['age'].max()) if 'age' in patients_df.columns else 0,
                'gender_distribution': gender_counts.to_dict() if len(gender_counts) > 0 else {}
            }
            
            if 'blood_group' in patients_df.columns and not patients_df['blood_group'].mode().empty:
                stats['most_common_blood_group'] = str(patients_df['blood_group'].mode().iloc[0])
            else:
                stats['most_common_blood_group'] = 'N/A'
            
            return self._convert_numpy_types(stats)
            
        except Exception as e:
            print(f"Error generating patient statistics: {e}")
            traceback.print_exc()
            return {"error": str(e)}
    
    def generate_appointment_analytics(self):
        """Generate appointment statistics and charts"""
        print("Generating appointment analytics...")
        
        try:
            appointments_df = self.dm.get_all_appointments()
            
            if appointments_df.empty or len(appointments_df) == 0:
                print("No appointment data available")
                return {"error": "No appointment data available", "total_appointments": 0}
            
            # 1. Appointment Status Distribution
            status_counts = appointments_df['status'].value_counts()
            if len(status_counts) > 0:
                fig1 = px.pie(
                    values=status_counts.values, 
                    names=status_counts.index,
                    title='Appointment Status Distribution',
                    color_discrete_sequence=px.colors.qualitative.Pastel
                )
                fig1.update_traces(textposition='inside', textinfo='percent+label')
                fig1.write_html(os.path.join(self.viz_dir, 'appointment_status.html'))
                print(f"Generated {os.path.join(self.viz_dir, 'appointment_status.html')}")
            
            # 2. Department-wise Appointments
            if 'department' in appointments_df.columns:
                dept_counts = appointments_df['department'].value_counts()
                if len(dept_counts) > 0:
                    fig2 = px.bar(
                        x=dept_counts.index, 
                        y=dept_counts.values,
                        title='Appointments by Department',
                        labels={'x': 'Department', 'y': 'Number of Appointments'},
                        color=dept_counts.values,
                        color_continuous_scale='Blues'
                    )
                    fig2.write_html(os.path.join(self.viz_dir, 'department_appointments.html'))
                    print(f"Generated {os.path.join(self.viz_dir, 'department_appointments.html')}")
            
            # Calculate statistics
            stats = {
                'total_appointments': len(appointments_df),
                'scheduled_appointments': len(appointments_df[appointments_df['status'] == 'Scheduled']) if 'status' in appointments_df.columns else 0,
                'completed_appointments': len(appointments_df[appointments_df['status'] == 'Completed']) if 'status' in appointments_df.columns else 0,
                'department_distribution': dept_counts.to_dict() if 'department' in appointments_df.columns and len(dept_counts) > 0 else {}
            }
            
            if 'department' in appointments_df.columns and len(dept_counts) > 0:
                stats['top_department'] = str(dept_counts.index[0])
            else:
                stats['top_department'] = 'N/A'
            
            return self._convert_numpy_types(stats)
            
        except Exception as e:
            print(f"Error generating appointment analytics: {e}")
            traceback.print_exc()
            return {"error": str(e)}
    
    def generate_financial_reports(self):
        """Generate billing and financial reports"""
        print("Generating financial reports...")
        
        try:
            billing_df = self.dm.get_all_bills()
            
            if billing_df.empty or len(billing_df) == 0:
                print("No billing data available")
                return {"error": "No billing data available", "total_revenue": 0}
            
            # 1. Revenue by Service Type
            if 'service_type' in billing_df.columns:
                revenue_by_service = billing_df.groupby('service_type')['amount'].sum()
                if len(revenue_by_service) > 0:
                    fig1 = px.pie(
                        values=revenue_by_service.values, 
                        names=revenue_by_service.index,
                        title='Revenue Distribution by Service Type',
                        color_discrete_sequence=px.colors.qualitative.Set2
                    )
                    fig1.update_traces(textposition='inside', textinfo='percent+label')
                    fig1.write_html(os.path.join(self.viz_dir, 'revenue_by_service.html'))
                    print(f"Generated {os.path.join(self.viz_dir, 'revenue_by_service.html')}")
            
            # 2. Payment Status
            if 'status' in billing_df.columns:
                status_counts = billing_df['status'].value_counts()
                if len(status_counts) > 0:
                    fig2 = px.bar(
                        x=status_counts.index, 
                        y=status_counts.values,
                        title='Bill Payment Status Distribution',
                        labels={'x': 'Payment Status', 'y': 'Number of Bills'},
                        color=status_counts.values,
                        color_continuous_scale='Reds'
                    )
                    fig2.write_html(os.path.join(self.viz_dir, 'payment_status.html'))
                    print(f"Generated {os.path.join(self.viz_dir, 'payment_status.html')}")
            
            # Calculate statistics
            stats = {
                'total_revenue': float(billing_df['amount'].sum()) if 'amount' in billing_df.columns else 0,
                'total_bills': len(billing_df),
                'pending_amount': float(billing_df[billing_df['status'] == 'Pending']['amount'].sum()) if 'status' in billing_df.columns and 'amount' in billing_df.columns else 0,
                'paid_amount': float(billing_df[billing_df['status'] == 'Paid']['amount'].sum()) if 'status' in billing_df.columns and 'amount' in billing_df.columns else 0,
                'average_bill_amount': float(billing_df['amount'].mean()) if 'amount' in billing_df.columns and not billing_df['amount'].isna().all() else 0
            }
            
            if 'service_type' in billing_df.columns and len(revenue_by_service) > 0:
                stats['most_profitable_service'] = str(revenue_by_service.idxmax())
            else:
                stats['most_profitable_service'] = 'N/A'
            
            return self._convert_numpy_types(stats)
            
        except Exception as e:
            print(f"Error generating financial reports: {e}")
            traceback.print_exc()
            return {"error": str(e)}
    
    def generate_medical_analytics(self):
        """Generate medical records analytics"""
        print("Generating medical analytics...")
        
        try:
            # Read medical records directly from file
            medical_file = os.path.join(self.dm.data_dir, 'medical_records.csv')
            if os.path.exists(medical_file):
                medical_df = pd.read_csv(medical_file)
            else:
                print("No medical records data available")
                return {"error": "No medical records data available", "total_medical_records": 0}
            
            if medical_df.empty or len(medical_df) == 0:
                print("No medical records data available")
                return {"error": "No medical records data available", "total_medical_records": 0}
            
            # 1. Common Diagnoses
            if 'diagnosis' in medical_df.columns:
                diagnosis_counts = medical_df['diagnosis'].value_counts().head(10)
                if len(diagnosis_counts) > 0:
                    fig1 = px.bar(
                        x=diagnosis_counts.values, 
                        y=diagnosis_counts.index,
                        orientation='h',
                        title='Top 10 Common Diagnoses',
                        labels={'x': 'Frequency', 'y': 'Diagnosis'},
                        color=diagnosis_counts.values,
                        color_continuous_scale='Oranges'
                    )
                    fig1.write_html(os.path.join(self.viz_dir, 'common_diagnoses.html'))
                    print(f"Generated {os.path.join(self.viz_dir, 'common_diagnoses.html')}")
            
            stats = {
                'total_medical_records': len(medical_df),
                'diagnosis_distribution': diagnosis_counts.head(5).to_dict() if 'diagnosis' in medical_df.columns and len(diagnosis_counts) > 0 else {}
            }
            
            if 'diagnosis' in medical_df.columns and len(diagnosis_counts) > 0:
                stats['most_common_diagnosis'] = str(diagnosis_counts.index[0])
            else:
                stats['most_common_diagnosis'] = 'N/A'
            
            return self._convert_numpy_types(stats)
            
        except Exception as e:
            print(f"Error generating medical analytics: {e}")
            traceback.print_exc()
            return {"error": str(e)}
    
    def generate_dashboard_summary(self):
        """Generate comprehensive dashboard with all metrics"""
        print("Generating comprehensive dashboard...")
        
        try:
            # Get all stats
            patient_stats = self.generate_patient_statistics()
            appointment_stats = self.generate_appointment_analytics()
            financial_stats = self.generate_financial_reports()
            medical_stats = self.generate_medical_analytics()
            
            dashboard_data = {
                'patient_stats': patient_stats,
                'appointment_stats': appointment_stats,
                'financial_stats': financial_stats,
                'medical_stats': medical_stats,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # Create summary visualization
            summary_stats = {
                'Total Patients': dashboard_data['patient_stats'].get('total_patients', 0),
                'Total Appointments': dashboard_data['appointment_stats'].get('total_appointments', 0),
                'Total Revenue': dashboard_data['financial_stats'].get('total_revenue', 0),
                'Pending Bills': dashboard_data['financial_stats'].get('pending_amount', 0)
            }
            
            # Summary bar chart
            if any(v > 0 for v in summary_stats.values()):
                fig = px.bar(
                    x=list(summary_stats.keys()),
                    y=list(summary_stats.values()),
                    title='Hospital System Overview',
                    labels={'x': 'Metrics', 'y': 'Count/Amount'},
                    color=list(summary_stats.values()),
                    color_continuous_scale='Viridis'
                )
                fig.write_html(os.path.join(self.viz_dir, 'system_overview.html'))
                print(f"Generated {os.path.join(self.viz_dir, 'system_overview.html')}")
            
            # Save dashboard data as JSON
            json_path = os.path.join(self.dm.data_dir, 'dashboard_data.json')
            with open(json_path, 'w') as f:
                json.dump(dashboard_data, f, indent=2, default=str)
            
            print(f"Dashboard data saved to {json_path}")
            
            return dashboard_data
            
        except Exception as e:
            print(f"Error generating dashboard: {e}")
            traceback.print_exc()
            return {"error": str(e)}
    
    def generate_all_reports(self):
        """Generate all analytics and reports"""
        print("=" * 50)
        print("GENERATING ALL ANALYTICS AND REPORTS")
        print("=" * 50)
        
        print(f"Visualizations folder: {os.path.abspath(self.viz_dir)}")
        
        dashboard_data = self.generate_dashboard_summary()
        
        print("\n" + "=" * 50)
        print("ALL REPORTS GENERATED SUCCESSFULLY!")
        print("=" * 50)
        print(f"Check the '{self.viz_dir}' folder for HTML charts")
        print(f"Check '{self.dm.data_dir}/dashboard_data.json' for analytics data")
        
        # Count generated files
        viz_files = [f for f in os.listdir(self.viz_dir) if f.endswith('.html')]
        print(f"Generated {len(viz_files)} visualization files")
        
        # Show full paths
        print("\nGenerated files:")
        for file in viz_files:
            print(f"   • {os.path.join(self.viz_dir, file)}")
        
        return dashboard_data

# Test the analytics
if __name__ == "__main__":
    print("Testing HospitalAnalytics...")
    
    # Create data manager first
    from data_manager import HospitalDataManager
    dm = HospitalDataManager()
    
    # Create analytics
    analytics = HospitalAnalytics(dm)
    
    # Generate a simple report
    stats = analytics.generate_patient_statistics()
    print("\nPatient Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")