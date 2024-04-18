from django.db import models
from users.models import User

class Feedback(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feedback_details=models.TextField(max_length=100)
    feedback_provider=models.CharField(max_length=30)
    feedback_rating = models.IntegerField(null=True, blank=True)
    feedback_date=models.DateField()
    publish=models.BooleanField(default=False)


# Create your models here.
