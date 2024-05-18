from django.db import models
from users.models import EmpModule, User

class ApplyJob(models.Model):
    id=models.AutoField(primary_key=True)
    candidate=models.ForeignKey(User, on_delete=models.CASCADE)
    status=models.CharField(max_length=10,null=True)
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

class Scheduler(models.Model):
    id = models.AutoField(primary_key=True)
    candidate = models.ForeignKey(User, on_delete=models.CASCADE)
    scheduledDate = models.DateField()
    STATUSES = (
        ('pending', 'pending'),
        ('attempted', 'attempted'),

    )
    status = models.CharField(max_length=15, choices=STATUSES)
    ROUNDS = (
        (1, 'Round 1'),
        (2, 'Round 2'),
    )
    round = models.IntegerField(choices=ROUNDS)
    
    
class Questions(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.CharField(max_length=512, null=True)
    option1 = models.CharField(max_length=100, null=True)
    option2 = models.CharField(max_length=100, null=True)
    option3 = models.CharField(max_length=100, null=True)
    option4 = models.CharField(max_length=100, null=True)
    correctResponse = models.CharField(max_length=50, null=True)
    type = models.CharField(max_length=50,null=True)
    level = models.IntegerField(null=True)
    stream = models.ForeignKey('Stream', on_delete=models.CASCADE, null=True)

    
class Track(models.Model):
    id=models.AutoField(primary_key=True)
    candidate=models.ForeignKey(User, on_delete=models.CASCADE)
    currentStatus=models.CharField(max_length=100)
    round1=models.CharField(max_length=100)
    round2=models.CharField(max_length=100)
    round3=models.CharField(max_length=100)
    round4=models.CharField(max_length=100)
    
    
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
    scheduler=models.ForeignKey(Scheduler,null=True, on_delete=models.CASCADE)
    question = models.IntegerField(null=True)
        
class Exam(models.Model):
    candidate = models.ForeignKey(User, on_delete=models.CASCADE)
    question_id=models.IntegerField(null=True)
    candidateResponse = models.CharField(max_length=255)
    correctResponse = models.CharField(max_length=255)
    Date = models.DateField()          #need to modigy this Date to date
    ROUNDS = (
        (1, 'Round 1'),
        (2, 'Round 2'),
    )
    round = models.IntegerField(choices=ROUNDS, null=True)
    status = models.CharField(max_length=50, null=True)
    scheduler = models.ForeignKey(Scheduler, on_delete=models.CASCADE)    

class AuthorizationToEmployee(models.Model):
    emp= models.ForeignKey(User, on_delete=models.CASCADE, related_name='employee_authorizations')
    candidate = models.ForeignKey(User, on_delete=models.CASCADE, related_name='candidate_authorizations')


    
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

       
class Notification(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    date = models.DateField()
    STATUSES = (
        (1,'read'),
        (2,'unread'),
        ) 
    status = models.TextField(choices=STATUSES)
    jobId=models.IntegerField(null=True)
    jobName=models.CharField(max_length=100, null = True)
    currentStatus = models.CharField(max_length=30, null = True)

    
class Certification(models.Model):
    candidate = models.ForeignKey(User, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    certificateUrl = models.URLField()
    dateIssued = models.DateField()  
    
class AuthorizeToModule(models.Model):
    id = models.AutoField(primary_key=True)
    employee=models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    module=models.ForeignKey(EmpModule, on_delete=models.CASCADE)           