from django.contrib import admin
from django.urls import include, path
from skill import views


urlpatterns = [
    path('', views.index, name='index'),path('jobseeker', views.jobseeker, name='jobseeker'),path('company', views.company, name='company'),
]