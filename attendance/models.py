from django.db import models
from users.models import User
class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date=models.DateField()
    in_time=models.TimeField()
    out_time=models.TimeField()       
    #here i also have to make a field for total hours

# Create your models here.
