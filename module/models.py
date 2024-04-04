from django.db import models
from users.models import User
from project.models import Project
class Module(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    module_name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()
    assigned_hours = models.DecimalField(max_digits=5, decimal_places=2)
    actual_hours = models.DecimalField(max_digits=5, decimal_places=2)


# Create your models here.
