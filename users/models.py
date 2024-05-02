from django.db import models
from django.db.models.signals import post_migrate
from django.dispatch import receiver



class EmpID(models.Model):
    id = models.AutoField(primary_key=True)
    emp_id = models.IntegerField(unique=True)

    def __str__(self):
        return str(self.emp_id)

class User(models.Model):
    id = models.AutoField(primary_key=True)
    emp = models.OneToOneField(EmpID, null=True, on_delete=models.CASCADE)

    userName = models.CharField(max_length=100, null = True)
    fullName = models.CharField(max_length=100, null=True)
    address=models.TextField(null=True)
    degree=models.CharField(max_length=100, null=True)
    # lastName = models.CharField(max_length=100, null=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=100, default='candidate')  #there will be three roles- admin,candidate, employee
    mobileNumber = models.CharField(unique=True, max_length=15)
    password = models.CharField(max_length=255, null=True)
    cv_url=models.URLField(null=True)
    active = models.BooleanField(default=False)


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
