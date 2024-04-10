from django.db import models


class User(models.Model):
    employeeID=models.IntegerField(unique=True,null=False)
    last_name = models.CharField(max_length=30,null=False)
    first_name = models.CharField(max_length=30, null=False)
    phone_number=models.IntegerField(unique=True,null=False)
    address=models.CharField(max_length=100,null=False)
    role=models.CharField(max_length=30,default='employee')
    email=models.EmailField(max_length=30,null=False,unique=True)
    password=models.TextField(null=False) 


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
    
class EmployeeID(models.Model):
    employeeID=models.IntegerField(unique=True,null=False)
# Create your models here.