from django.db import models
import uuid
from django.contrib.auth.models import User


class Patient(models.Model):

    STATUS_TYPE = (
        ('Married', 'Married'),
        ('Not Married', 'Not Married'),
    )

    BLOOD_TYPE = (
        ('A', 'A'),
        ('B', 'B'),
        ('O', 'O'),
        ('AB', 'AB'),
    )

    user=models.OneToOneField(User,on_delete=models.CASCADE)
    date_of_birth = models.DateField('Date of birth')
    iin_number = models.CharField('IIN', max_length = 12)
    id_number = models.BigAutoField(primary_key = True)
    #id_number = models.UUIDField(default = uuid.uuid4, unique = True, primary_key = True, editable = False)
    blood_group = models.CharField('Blood group', max_length = 5, choices = BLOOD_TYPE)
    emergency_contact_number = models.CharField('Emergency contact number', max_length = 12)
    contact_number = models.CharField('Contact Number', max_length = 12)
    email = models.EmailField('Email address', max_length = 254)
    address = models.CharField('Physical address', max_length = 1024)
    martial_status = models.CharField('Martial status', max_length = 20, choices = STATUS_TYPE)
    registration_date = models.DateTimeField(auto_now_add = True)
    

    def __str__(self):
        return self.user.first_name + self.user.last_name


    class Meta:
        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'


class Doctor(models.Model):
    DEGREE_OF_EDUCATION = (
        ('No Education', 'No Education'),
        ('High School Diploma', 'High School Diploma'),
        ('Certificate or associate degree', 'Certificate or associate degree'),
        ("Bachelor's Degree", "Bachelor's Degree"),
        ("Master's Degree", "Master's Degree"),
        ('Doctorate', 'Doctorate'),
    )

    RATING = (
        ('0', '0'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
    )

    user=models.OneToOneField(User,on_delete=models.CASCADE)
    date_of_birth = models.DateField('Date of birth')
    iin_number = models.CharField('IIN', max_length = 12)
    id_number = models.BigAutoField(primary_key = True)
    #id_number = models.UUIDField(default = uuid.uuid4, unique = True, primary_key = True, editable = False)
    contact_number = models.CharField('Contact Number', max_length = 12)
    department_id = models.ForeignKey('Department', on_delete=models.CASCADE)
    specialization_details_id = models.ForeignKey('Specialization', on_delete=models.CASCADE)
    experience = models.CharField('Experience In Years', max_length = 4)
    photo = models.ImageField(null = True, blank = False, upload_to = 'images/', default='images/download.png')
    category = models.CharField('Category', max_length = 100)
    price = models.DecimalField('Price', max_digits = 10, decimal_places = 2)
    education = models.CharField('Degree of Education', max_length = 50, choices = DEGREE_OF_EDUCATION)
    rating = models.CharField('Rating', max_length = 3, choices = RATING)
    address = models.CharField('Address', max_length = 1024)

    

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name 
    

    class Meta:
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctors'


class Appointment(models.Model):
    class Meta:
        verbose_name = 'Appointment'
        verbose_name_plural = 'Appointments'
        unique_together = ('doctor', 'date', 'timeslot')

    TIMESLOT_LIST = (
        (0, '09:00 – 09:30'),
        (1, '10:00 – 10:30'),
        (2, '11:00 – 11:30'),
        (3, '12:00 – 12:30'),
        (4, '13:00 – 13:30'),
        (5, '14:00 – 14:30'),
        (6, '15:00 – 15:30'),
        (7, '16:00 – 16:30'),
        (8, '17:00 – 17:30'),
    )

    doctor = models.ForeignKey('Doctor', on_delete = models.CASCADE, related_name='docs')
    date = models.DateField(help_text="YYYY-MM-DD")
    timeslot = models.IntegerField(choices=TIMESLOT_LIST)
    patient_name = models.CharField(max_length=60)
    email = models.EmailField(max_length=200)
    phone = models.CharField(max_length=12)

    def __str__(self):
        return '{} {} {}. Patient: {}'.format(self.date, self.time, self.doctor, self.patient_name)

    @property
    def time(self):
        return self.TIMESLOT_LIST[self.timeslot][1]


class Specialization(models.Model):
    id = models.BigAutoField(primary_key=True)
    specialization = models.CharField(max_length=100)

    def __str__(self):
        return self.specialization

    class Meta:
        verbose_name = 'Specialization'
        verbose_name_plural = 'Specializations'



class Department(models.Model):
    id = models.BigAutoField(primary_key=True)
    department = models.CharField(max_length=100)

    def __str__(self):
        return self.department

    class Meta:
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'


class Preappointment(models.Model):
    class Meta:
        verbose_name = 'Pre-appointment'
        verbose_name_plural = 'Pre-appointments'
        unique_together = ('doctor_id', 'date', 'timeslot')

    TIMESLOT_LIST = (
        (0, '09:00 – 09:30'),
        (1, '10:00 – 10:30'),
        (2, '11:00 – 11:30'),
        (3, '12:00 – 12:30'),
        (4, '13:00 – 13:30'),
        (5, '14:00 – 14:30'),
        (6, '15:00 – 15:30'),
        (7, '16:00 – 16:30'),
        (8, '17:00 – 17:30'),
    )

    doctor_id = models.IntegerField()
    date = models.DateField(help_text="YYYY-MM-DD")
    timeslot = models.IntegerField(choices=TIMESLOT_LIST)
    patient_name = models.CharField(max_length=60)
    email = models.EmailField(max_length=200)
    phone = models.CharField(max_length=12)

    def __str__(self):
        return '{} {} {}. Patient: {}'.format(self.date, self.time, self.doctor_id, self.patient_name)

    @property
    def time(self):
        return self.TIMESLOT_LIST[self.timeslot][1]