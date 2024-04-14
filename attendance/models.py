from django.db import models
from users.models import User
class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date=models.DateField()
    in_time=models.TimeField()
    out_time=models.TimeField()

# Create your models here.
