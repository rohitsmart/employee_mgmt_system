from django.db import models
from users.models import User

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task_name=models.CharField(max_length=30)
    status=models.CharField(max_length=30)


# Create your models here.
