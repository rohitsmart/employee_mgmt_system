from django.db import models
from users.models import User
# from recruit.models import Questions

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
    question_id=models.IntegerField(null=True)
    correctAnswer=models.CharField(max_length=50, null=True)
    candidate_answer=models.CharField(max_length=100, null=True)
    TYPE_CHOICES = (
        ('mcq', 'Multiple Choice Question'),
        ('subjective', 'Subjective Question'),
    )
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, null=True)
    LEVEL_CHOICES = (
        (1, 'Level 1'),
        (2, 'Level 2'),
        (3, 'Level 3'),
    )
    level = models.IntegerField(choices=LEVEL_CHOICES,null=True)
    stream =models.ForeignKey(Stream, on_delete=models.CASCADE, null=True)
    
class Track(models.Model):
    id=models.AutoField(primary_key=True)
    candidate=models.ForeignKey(User, on_delete=models.CASCADE)
    currrentStatus=models.CharField(max_length=100)
    round1=models.CharField(max_length=100)
    round2=models.CharField(max_length=100)
    round3=models.CharField(max_length=100)
    round4=models.CharField(max_length=100)
    
class Scheduler(models.Model):
    id=models.AutoField(primary_key=True)
    candidate=models.ForeignKey(User, on_delete=models.CASCADE)
    scheduledDate=models.DateField()
    STATUSES = (
        (1,'started'),
        (2,'completed'),
        (3,'todo'),
        (4,'inprogress'),
        (5,'disqualified'),
        ) 
    status = models.TextField(choices=STATUSES)
    ROUNDS = (
         (1, 'Round 1'),
         (2, 'Round 2'),
    )
    round = models.IntegerField(choices=ROUNDS)
      
    
class Result(models.Model):
    id=models.AutoField(primary_key=True)
    candidate=models.ForeignKey(User, on_delete=models.CASCADE)
    status=models.CharField(max_length=70)
    date=models.DateField()
    maximum=models.IntegerField(null=False)
    obtained=models.IntegerField(null=False)
    needed=models.IntegerField(null=False)
    ROUNDS = (
        (1, 'Round 1'),
        (2, 'Round 2'),
    )
    round = models.CharField(max_length=50,choices=ROUNDS)
    scheduler=models.ForeignKey(Scheduler, on_delete=models.CASCADE)
        
class Exam(models.Model):
    candidate = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    candidateResponse = models.CharField(max_length=255)
    correctResponse = models.CharField(max_length=255)
    Date = models.DateField()
    ROUNDS = (
        (1, 'Round 1'),
        (2, 'Round 2'),
    )
    round = models.IntegerField(choices=ROUNDS)
    status = models.CharField(max_length=50, null=True)
    scheduler = models.ForeignKey(Scheduler, on_delete=models.CASCADE)    

class AuthorizationToEmployee(models.Model):
    emp= models.ForeignKey(User, on_delete=models.CASCADE, related_name='employee_authorizations')
    candidate = models.ForeignKey(User, on_delete=models.CASCADE, related_name='candidate_authorizations')

    def __str__(self):
        return f"Authorization: {self.emp} to {self.candidate}"
    
class AuthorizationToModule(models.Model):
    emp = models.ForeignKey(User, on_delete=models.CASCADE, related_name='module_authorizations')

    def __str__(self):
        return f"Module Authorization: {self.emp}"    
    
class Job(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Expired', 'Expired'),
        ('Hide', 'Hide'),
        ('InActive', 'InActive'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='InActive')
    jobName = models.CharField(max_length=100)
    jobDescription = models.TextField()
    jobSkills = models.TextField()
    experience = models.IntegerField()
    expire = models.DateField()
    createdDate = models.DateField(auto_now_add=True)
    creater = models.ForeignKey(User, on_delete=models.CASCADE)    #this is associated with the user table
    
class Chat(models.Model):
    sender = models.ForeignKey(User, related_name='sent_chats', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_chats', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    deletedAt = models.DateTimeField(blank=True, null=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Chat between {self.sender} and {self.receiver}" 
       
class Notification(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    date = models.DateField()
    STATUSES = (
        (1,'read'),
        (2,'unread'),
        ) 
    status = models.TextField(choices=STATUSES)

    def __str__(self):
        return f"Notification for {self.user}" 
    
class Certification(models.Model):
    candidate = models.ForeignKey(User, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    certificateUrl = models.URLField()
    dateIssued = models.DateField()

    def __str__(self):
        return f"Certification for {self.candidate}"       

             
        

# Create your models here.
