from django.db import models
from users.models import User

class ApplyJob(models.Model):
    id=models.AutoField(primary_key=True)
    candidate=models.ForeignKey(User, on_delete=models.CASCADE)
    jobID=models.CharField(max_length=100)
    
class Role(models.Model):
    id=models.AutoField(primary_key=True)
    roleName=models.CharField(max_length=100, unique=True)
    
class EmpRole(models.Model):
    id=models.AutoField(primary_key=True)
    roleName=models.CharField(max_length=50)   
    
class Stream(models.Model):
    id=models.AutoField(primary_key=True)
    streamName=models.CharField(max_length=100, unique=True)
    
class Questions(models.Model):
    id=models.AutoField(primary_key=True)
    question=models.CharField(max_length=500,unique=True)
    option1=models.TextField()
    option2=models.TextField()
    option3=models.TextField()
    option4=models.TextField()
    correctAnswer=models.CharField(max_length=50)
    TYPE_CHOICES = (
        ('mcq', 'Multiple Choice Question'),
        ('subjective', 'Subjective Question'),
    )
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    LEVEL_CHOICES = (
        (1, 'Level 1'),
        (2, 'Level 2'),
        (3, 'Level 3'),
    )
    level = models.IntegerField(choices=LEVEL_CHOICES)
    stream =models.ForeignKey(Stream, on_delete=models.CASCADE)
    
class Track(models.Model):
    id=models.AutoField(primary_key=True)
    candidate=models.ForeignKey(User, on_delete=models.CASCADE)
    currrentStatus=models.CharField(max_length=100)
    round1=models.CharField(max_length=100)
    round2=models.CharField(max_length=100)
    round3=models.CharField(max_length=100)
    round4=models.CharField(max_length=100)
       
    
    
             
        

# Create your models here.
