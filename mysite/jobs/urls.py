from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('jobs/<int:pk>/', views.DetailView.as_view(), name='job_details'),
    path('jobs/<int:job_id>/apply/', views.ApplyView.as_view(), name='apply'),
    path('jobs/<int:job_id>/applicant_details/', views.Details.as_view(), name='applicant_details'),
     path('jobs/applicant_details/questions/', views.Questions.as_view(), name='questions'),
    path('applicant_details/questions/final/', views.answerValidate.as_view(), name='final'),
]

