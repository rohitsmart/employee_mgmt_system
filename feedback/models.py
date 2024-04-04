from django.db import models
from users.models import User

class Feedback(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feedback_type=models.CharField(max_length=30)
    feedback_details=models.TextField(max_length=100)
    feedback_date=models.DateField()
    feedback_provider=models.CharField(max_length=30)
    feedback_rating = models.IntegerField(null=True, blank=True)
    status=models.CharField(max_length=30)
    action_taken=models.TextField()

# Create your models here.
