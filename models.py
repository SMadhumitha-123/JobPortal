from django.db import models
from django.contrib.auth.models import User
class Company(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.name
class Job(models.Model):
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    job_type = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.title
class JobApplication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='user_applications')
    job = models.ForeignKey(Job, on_delete=models.CASCADE)  
    cv = models.FileField(upload_to='cvs/')
    applied_on = models.DateTimeField(auto_now_add=True)
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    def __str__(self):
        return f"{self.user.username} applied for {self.job.title}"
