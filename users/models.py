from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    address=models.CharField(max_length=100)
    email=models.EmailField(max_length=30)
    password=models.CharField(max_length=30)
    role=models.CharField(max_length=30,default='employee')

class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date=models.DateField()
    in_time=models.TimeField()
    out_time=models.TimeField()

class Device(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    device_name = models.CharField(max_length=30)
    device_type = models.CharField(max_length=30)
    location = models.CharField(max_length=100)  

    # Create your models here.
