from django.contrib import admin
from . models import Patient, Doctor, Appointment, Specialization, Department, Preappointment


admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Appointment)
admin.site.register(Specialization)
admin.site.register(Department)
admin.site.register(Preappointment)
