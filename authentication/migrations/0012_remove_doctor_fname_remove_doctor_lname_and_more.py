# Generated by Django 4.1.3 on 2022-12-06 21:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0011_remove_patient_fname_remove_patient_lname_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctor',
            name='fname',
        ),
        migrations.RemoveField(
            model_name='doctor',
            name='lname',
        ),
        migrations.RemoveField(
            model_name='doctor',
            name='mname',
        ),
        migrations.RemoveField(
            model_name='doctor',
            name='schedule_details',
        ),
    ]
