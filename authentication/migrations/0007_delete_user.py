# Generated by Django 4.1.3 on 2022-12-06 17:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0006_alter_doctor_date_of_birth_alter_doctor_photo_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]
