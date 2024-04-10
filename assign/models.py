from django.db import models
from users.models import User
from project.models import Project
from module.models import Module
from task.models import Task

class Assign(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    assign_date=models.DateField()
    assigned_by=models.CharField(max_length=30)
    deadline=models.DateField()
    status=models.CharField(max_length=30)
    comment=models.TextField()

# Create your models here.