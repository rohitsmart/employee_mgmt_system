from django.db import models
from users.models import User
class Device(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    device_name = models.CharField(max_length=30)
    device_type = models.CharField(max_length=30)
    deviceID=models.CharField(max_length=100)
    location = models.CharField(max_length=100)



# Create your models here.
