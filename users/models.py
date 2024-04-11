from django.db import models

class EmpID(models.Model):
    id = models.AutoField(primary_key=True)
    emp_id = models.IntegerField(unique=True)

    def __str__(self):
        return str(self.emp_id)

class User(models.Model):
    id = models.AutoField(primary_key=True)
    emp_id = models.OneToOneField(EmpID, on_delete=models.CASCADE)
    firstName = models.CharField(max_length=100, null=True)
    lastName = models.CharField(max_length=100, null=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=100, null=True)
    mobileNumber = models.CharField(unique=True, max_length=15)
    password = models.CharField(max_length=255)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.email
