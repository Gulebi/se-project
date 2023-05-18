from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name="home"),
    path('adminpage', views.adminpage, name="adminpage"),
    path('patient', views.patient, name="patient"),
    path('doctor', views.doctor, name="doctor"),
    path('signin', views.signin, name="signin"),
    path('signout', views.signout, name="signout"),

    path('update_patient/<patient_id>', views.update_patient, name="update-patient"),
    path('delete_patient/<patient_id>', views.delete_patient, name="delete-patient"),

    path('update_doctor/<doctor_id>', views.update_doctor, name="update-doctor"),
    path('delete_doctor/<doctor_id>', views.delete_doctor, name="delete-doctor"),

    path('make_appointment/', views.make_appointment, name="make-appointment"),
    path('appointment/', views.appointment, name="appointment"),
    path('specialization/', views.specialization, name="specialization"),
    path('confirm_appointment/', views.confirm_appointment, name="confirm-appointment"),

    path('delete_preappointment/<doctor_id>/<date>/<timeslot>', views.delete_preappointment, name="delete-preappointment"),
    path('confirm_request/<doctor_id>/<date>/<timeslot>', views.confirm_request, name="confirm-request"),

    path('search_doctor', views.search_doctor, name="search-doctor"),
    path('personal_page/<username>', views.personal_page, name="personal-page"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)