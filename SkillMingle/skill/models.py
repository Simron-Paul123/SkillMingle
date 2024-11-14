# models.py
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    # description = models.TextField()  # Removed or commented this line
    icon_class = models.CharField(max_length=50, help_text="CSS class for icon, e.g., 'ri-pencil-ruler-2-fill'")

    def job_count(self):
        # Count the number of jobs associated with this category
        return self.jobs.count()

    def __str__(self):
        return self.name  # Optional for better readability in admin and other places

class Job(models.Model):
    company_logo = models.ImageField(upload_to='company_logos/', default='company_logos/default.png')
    company_name = models.CharField(max_length=100, default='Default Company Name')  # Default value for company_name
    location = models.CharField(max_length=100, default='Unknown Location')  # Default value for location
    title = models.CharField(max_length=100, default='Job Title')  # Default value for title
    description = models.TextField(default='Job Description not provided.')  # Default value for description
    positions = models.IntegerField(default=1)  # Default value for positions
    employment_type = models.CharField(max_length=50, default='Full Time')  # Default value for employment_type
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Default value for salary
    category = models.ForeignKey(Category, related_name='jobs', on_delete=models.CASCADE)

    def __str__(self):
        return self.title
