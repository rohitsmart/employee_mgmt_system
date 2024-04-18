from django.db import models



class EmpID(models.Model):
    id = models.AutoField(primary_key=True)
    emp_id = models.IntegerField(unique=True)

    def __str__(self):
        return str(self.emp_id)

class User(models.Model):
    id = models.AutoField(primary_key=True)
    emp_id = models.OneToOneField(EmpID, on_delete=models.CASCADE)
    userName = models.CharField(max_length=100, null = True)
    fullName = models.CharField(max_length=100, null=True)
    address=models.TextField()
    degree=models.CharField(max_length=100)
    # lastName = models.CharField(max_length=100, null=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=100, default='candidate')  #there will be three roles- admin,candidate, employee
    mobileNumber = models.CharField(unique=True, max_length=15)
    password = models.CharField(max_length=255)
    cv_url=models.URLField()
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.email
