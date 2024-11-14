from django.http import HttpResponse
from django.shortcuts import render

from .models import Category, Job

# Create your views here.
def index(request):
    return render(request,'index.html')
def jobseeker(request):
    jobs = Job.objects.all()  # Fetch all job entries from the Job model
    categories = Category.objects.all()  # Fetch all category entries from the Category model
    return render(request, 'job_seeker.html', {'jobs': jobs, 'categories': categories})
def company(request):
    return render(request, 'company.html')

