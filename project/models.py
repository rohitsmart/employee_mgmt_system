from django.db import models
from users.models import User

class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # who created this project
    project_name = models.CharField(max_length=100)
    description = models.TextField()
    number_of_module=models.CharField(max_length=30)
    start_date = models.DateField()
    end_date = models.DateField()
    status=models.CharField(max_length=30)

# Create your models here.
