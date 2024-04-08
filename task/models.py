from django.db import models
from users.models import User
from project.models import Project
from module.models import Module

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    task_name=models.CharField(max_length=30,null=True)
    task_detail=models.TextField()
    status=models.CharField(max_length=30)

# Create your models here.
