from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from . models import Patient, Doctor, Specialization, Appointment, Preappointment
from django.contrib.auth.decorators import login_required
from .forms import PatientForm, DoctorForm, AppointmentForm, PatientUserForm, DoctorUserForm
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required,user_passes_test

from django.core import serializers



def home(request):
    return render(request, "authentication/index.html")


def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()
def is_doctor(user):
    return user.groups.filter(name='DOCTOR').exists()
def is_patient(user):
    return user.groups.filter(name='PATIENT').exists()


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def adminpage(request):
    
    patients = Patient.objects.all()
    #patients_list = {'patients': patients}


    doctors = Doctor.objects.all()
    #doctors_list = {'doctors': doctors}

    return render(request, "authentication/adminpage.html", {'patients': patients, 'doctors': doctors})


def update_patient(request, patient_id):
    patient = Patient.objects.get(id_number = patient_id)
    
    form = PatientForm(request.POST or None, instance = patient)

    if form.is_valid():
        form.save()
        return redirect('adminpage')
    return render(request, "authentication/update_patient.html", {'patient': patient, 'form': form})


def delete_patient(request, patient_id):
    patient = Patient.objects.get(id_number = patient_id)
    user = User.objects.filter(username = patient.user.username)
    user.delete()
    patient.delete()

    return redirect('adminpage')


@login_required
def patient(request):
    
    userForm = PatientUserForm()
    patientForm = PatientForm()
    mydict={'userForm':userForm,'patientForm':patientForm}

    if request.method == "POST":
        userForm = PatientUserForm(request.POST)
        patientForm = PatientForm(request.POST,request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            patient = patientForm.save(commit=False)
            patient.user = user
            patient = patient.save()
            my_patient_group = Group.objects.get_or_create(name='PATIENT')
            my_patient_group[0].user_set.add(user)
            return redirect ('adminpage')
        

    return render(request, "authentication/patient.html", context = mydict)



def update_doctor(request, doctor_id):
    doctor = Doctor.objects.get(id_number = doctor_id)
    
    form = DoctorForm(request.POST or None, instance = doctor)

    if form.is_valid():
        form.save()
        return redirect('adminpage')
    return render(request, "authentication/update_doctor.html", {'doctor': doctor, 'form': form})


def delete_doctor(request, doctor_id):
    doctor = Doctor.objects.get(id_number = doctor_id)
    user = User.objects.filter(username = doctor.user.username)
    user.delete()
    doctor.delete()

    return redirect('adminpage')


@login_required
def doctor(request):
       
    userForm = DoctorUserForm()
    doctorForm = DoctorForm()
    mydict={'userForm':userForm,'doctorForm':doctorForm}
    if request.method == "POST":
        userForm = DoctorUserForm(request.POST)
        doctorForm = DoctorForm(request.POST,request.FILES)
        if userForm.is_valid() and doctorForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            doctor = doctorForm.save(commit=False)
            doctor.user = user
            doctor=doctor.save()
            my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
            my_doctor_group[0].user_set.add(user)
            return redirect ('adminpage')
        

    return render(request, "authentication/doctor.html", context=mydict)


def signin(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username = username, password = password)

        if user is not None: 
            login(request, user)
            #fname = user.first_name
            messages.success(request, f' welcome {username}!! ')
            return redirect('home')
        
        else:
            messages.info(request, 'account does not exists')
            return HttpResponseRedirect('signin')

    return render(request, "authentication/signin.html")

def signout(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('home')


def make_appointment(request):
    doctors = Doctor.objects.filter()

    if request.method == "POST":
        doc = request.POST["doctor"]
        doctor = Doctor.objects.get(id_number = doc)
        date = request.POST["date"]
        timeslot = request.POST["timeslot"]
        patient_name = request.POST["name"]
        phone = request.POST["phone"]
        email = request.POST["email"]

        if Appointment.objects.filter(doctor=doctor, date=date, timeslot=timeslot):
            messages.error(request, "Timeslot is not available")
            return redirect('make-appointment')
        else:
            myappointment = Preappointment.objects.create(doctor_id=doc, date=date, timeslot=timeslot,
                                                       patient_name=patient_name, phone=phone, email=email)
            myappointment.save()
            messages.success(request, "Your appointment has been send to the administrator. You will receive your confirmation very soon!")


    context = {
        'doctors': doctors,
    }

    return render(request, "authentication/make_appointment.html", context)

def confirm_appointment(request):
    appointments = Preappointment.objects.filter()
    doctors = Doctor.objects.filter()
    context = {
        'appointments': appointments,
        'doctors': doctors,
    }
    return render(request, "authentication/confirm_appointment.html", context)

def appointment(request):
    patients = Patient.objects.all()

    data = serializers.serialize('json', patients)

    return render(request, "authentication/appointment.html", {'patients': patients, "data": data})

def specialization(request):
    doctors = Doctor.objects.filter()
    specializations = Specialization.objects.filter()
    appointments = Appointment.objects.filter()

    context = {
        'doctors': doctors,
        'specializations': specializations,
        'appointments': appointments,
    }
    return render(request, "authentication/specialization.html", context)

def delete_preappointment(request, doctor_id, date, timeslot):
    preappointment = Preappointment.objects.get(doctor_id=doctor_id, date=date, timeslot=timeslot)
    preappointment.delete()

    return redirect('confirm-appointment')

def confirm_request(request, doctor_id, date, timeslot):
    doctors = Doctor.objects.get(id_number=doctor_id)
    appointments = Preappointment.objects.get(doctor_id=doctor_id, date=date, timeslot=timeslot)
    if request.method == "POST":
        doc = appointments.doctor_id
        doctor = Doctor.objects.get(id_number = doc)
        date = appointments.date
        timeslot = appointments.timeslot
        patient_name = appointments.patient_name
        phone = appointments.phone
        email = appointments.email

        if Appointment.objects.filter(doctor=doctor, date=date, timeslot=timeslot):
            messages.error(request, "Timeslot is not available")
            return redirect('make-appointment')
        else:
            myappointment = Appointment.objects.create(doctor=doctor, date=date, timeslot=timeslot,
                                                       patient_name=patient_name, phone=phone, email=email)
            myappointment.save()
            preappointment = Preappointment.objects.get(doctor_id=doctor_id, date=date, timeslot=timeslot)
            preappointment.delete()
            messages.success(request, "Appointment was set successfully")


    context = {
        'doctors': doctors,
        'appointments': appointments
    }

    return render(request, "authentication/confirm_request.html", context)


def personal_page(request, username):
    user = User.objects.get(username = username)
    return render(request, "authentication/personal_page.html", {'user': user})


def search_doctor(request):
    if request.method == "POST":
        searched = request.POST['searched']
        doctors = User.objects.filter(first_name__contains = searched)
        specializations = Specialization.objects.filter(specialization__contains=searched)
        hold_doctors = Doctor.objects.filter()

        context = {
            'searched': searched,
            'doctors': doctors,
            'specializations': specializations,
            'hold_doctors': hold_doctors,
        }

        return render(request, "authentication/search_doctor.html", context)
    else:
        return render(request, "authentication/search_doctor.html", {})
