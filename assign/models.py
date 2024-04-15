from django.db import models
from users.models import User
from project.models import Project
from module.models import Module
from task.models import Task

class Assign(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)      #here user is the user which is assigning the task
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    assigned_by=models.CharField(max_length=30)
    assigned_to=models.CharField(max_length=30)
    assign_date=models.DateField()
    deadline=models.DateField()
    status=models.CharField(max_length=30)
    comment=models.TextField()

# Create your models here.