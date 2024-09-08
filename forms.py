from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Job
from .models import JobApplication
from django.core.files.storage import FileSystemStorage

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'job_type','company']
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
class JobSearchForm(forms.Form):
    title = forms.CharField(label='Job Title', max_length=100, required=False)
class JobApplicationForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    cv = forms.FileField()