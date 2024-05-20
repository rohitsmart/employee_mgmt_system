from django.db import models
from django.db.models.signals import post_migrate
from django.dispatch import receiver


class EmpID(models.Model):
    id = models.AutoField(primary_key=True)
    emp_id = models.IntegerField(unique=True)
    designation = models.CharField(max_length=100, null = True)

class User(models.Model):
    id = models.AutoField(primary_key=True)
    firstName = models.CharField(max_length=100, null=True)
    lastName = models.CharField(max_length=100, null=True)
    emp = models.OneToOneField(EmpID, null=True, on_delete=models.CASCADE)
    userName = models.CharField(max_length=100, null = True)
    fullName = models.CharField(max_length=100, null=True)
    address=models.TextField(null=True)
    degree=models.CharField(max_length=100, null=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=100, default='candidate')  
    mobileNumber = models.BigIntegerField(unique=False)
    password = models.CharField(max_length=512, null=True)
    cv_url=models.URLField(null=True)
    img_url=models.URLField(null=True)
    active = models.BooleanField(default=False)

class EmpModule(models.Model):
    id = models.AutoField(primary_key=True)
    moduleName=models.CharField(max_length=100,null=True)
    moduleKey=models.TextField()

class Token(models.Model):
    token = models.CharField(max_length=255, unique=True)
    user_id =models.IntegerField()   

@receiver(post_migrate)
def create_admin(sender, **kwargs):
    if not User.objects.filter(role='admin').exists():
        User.objects.create(
            userName='admin',
            fullName='Admin',
            email='admin@gmail.com',
            role='admin',
            mobileNumber='7856987456',
            password='password'
        )
