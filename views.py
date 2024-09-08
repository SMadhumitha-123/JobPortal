from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import LoginForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import IntegrityError
from django.contrib.auth.models import User
from .models import Job
from .forms import JobForm
from .forms import JobSearchForm
from .models import Company
from .models import Job, JobApplication
from .forms import JobApplicationForm
from django.contrib import messages
def is_admin(user):
    return user.is_superuser
def home(request):
    return render(request, 'jobs/home.html') 
def employee_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('job_list')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

def employee_logout(request):
    logout(request)
    return redirect('employee_login')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('job_list')  
    else:
        form = UserCreationForm()
    return render(request, 'registration/sign_up.html', {'form': form})

    
@login_required
def job_list(request):
    jobs = Job.objects.none()
    search_query = request.GET.get('q')
    job_type_filter = request.GET.get('job_type')

    if search_query or job_type_filter:
        jobs = Job.objects.all()  

        if search_query:
            jobs = jobs.filter(title__icontains=search_query) 

        if job_type_filter:
            jobs = jobs.filter(job_type=job_type_filter)  

    return render(request, 'jobs/job_list.html', {'jobs': jobs})
@login_required
def apply_job(request, job_id):
   
    job = Job.objects.get(id=job_id)
    if request.method == 'POST':    
        form = JobApplicationForm(request.POST, request.FILES) 
        if form.is_valid():         
            messages.success(request, 'Successfully registered for the job!')          
            return redirect('application_success') 
        else:
            messages.error(request, 'There was an error with your application.')

    else:
        form = JobApplicationForm()

    return render(request, 'jobs/apply_job.html', {'job': job, 'form': form})
@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user
            job.save()
            return redirect('job_list')
    else:
        form = JobForm()
    return render(request, 'jobs/add_job.html', {'form': form})
def delete_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    job.delete()
    return redirect('job_list')
def search_job(request):
    query = request.GET.get('q')
    if query:
        jobs = Job.objects.filter(title__icontains=query)
    else:
        jobs = Job.objects.all()
    
    return render(request, 'jobs/job_list.html', {'jobs': jobs})
@login_required
@user_passes_test(lambda u: u.is_superuser)
def edit_job(request, job_id):
    job = Job.objects.get(id=job_id)
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('job_list')
    else:
        form = JobForm(instance=job)
    return render(request, 'jobs/edit_job.html', {'form': form})

def application_success(request):
    return render(request, 'jobs/application_success.html')
def publish_job(request, job_id):
    job = Job.objects.get(id=job_id)
    if request.user.is_superuser:
        job.published = True
        job.save()
    return redirect('job_list')

def unpublish_job(request, job_id):
    job = Job.objects.get(id=job_id)
    if request.user.is_superuser:
        job.published = False
        job.save()
    return redirect('job_list')
def company_list(request):
    companies = Company.objects.all()
    return render(request, 'jobs/company_list.html', {'companies': companies})