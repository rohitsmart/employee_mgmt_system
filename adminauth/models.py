from django.db import models

class UserCredential(models.Model):
    username = models.CharField(unique=True,max_length=30)
    password = models.CharField(max_length=30)
    email = models.CharField(max_length=30)

# Create your models here.
