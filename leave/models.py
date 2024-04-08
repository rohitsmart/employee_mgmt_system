from django.db import models
from users.models import User
class Leave(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    leave_type=models.CharField(max_length=30)
    start_date=models.DateField()
    end_date=models.DateField()
    reason=models.CharField(max_length=30)
    status=models.CharField(max_length=30)

# Create your models here.
