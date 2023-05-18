from django import forms
from django.forms import ModelForm
from .models import Patient, Doctor, Appointment
from django.contrib.auth.models import User


class PatientUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
class PatientForm(ModelForm):
    class Meta:
        model = Patient
        fields = ('date_of_birth', 'iin_number', 'id_number', 'blood_group', 'emergency_contact_number', 'contact_number', 'email', 'address', 'martial_status')
        

class DoctorUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
class DoctorForm(ModelForm):
    class Meta:
        model = Doctor
        fields = ('date_of_birth', 'iin_number', 'contact_number', 'department_id', 'specialization_details_id', 'experience', 'photo', 'category', 'price', 'education', 'rating', 'address')
        


class AppointmentForm(ModelForm):
    class Meta:
        model = Appointment
        fields = ('doctor', 'date', 'timeslot')