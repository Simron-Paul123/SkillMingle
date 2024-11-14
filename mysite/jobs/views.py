from django.views import generic
from django.shortcuts import get_object_or_404, render, redirect
from jobs.eval import function
from .models import Applicant, Job, question, answer, Result
from .forms import JobForm, Question_Form
from .resume import extract_text_from_pdf, extract_skills, extract_name, extract_mobile_number, extract_email, get_matching_skills
from django.urls import reverse_lazy
import os
from . import eval
import cgi
import requests
from django.core.files.storage import FileSystemStorage


class IndexView(generic.ListView):
    template_name = 'jobs/index.html'

    def get_queryset(self):
        return Job.objects.all()


class DetailView(generic.DetailView):
    model = Job
    template_name = 'jobs/details.html'


class ApplyView(generic.CreateView):
    model = Applicant
    form_class = JobForm
    template_name = 'jobs/apply.html'
    
    def form_valid(self, form):
        # Get the job object based on the URL parameter (job_id)
        job = get_object_or_404(Job, id=self.kwargs['job_id'])
        
        # Associate the job with the applicant before saving
        applicant = form.save(commit=False)
        applicant.job = job
        applicant.save()
        
        # Redirect to the applicant details page after successful submission
        return super().form_valid(form)

    def get_success_url(self):
        # After successful form submission, redirect to applicant details page
        return reverse_lazy('applicant_details', kwargs={'job_id': self.kwargs['job_id']})


class Details(generic.ListView):
    template_name = 'jobs/applicant_details.html'
    resume_dir = "C:\\Users\\User\\OneDrive\\Desktop\\PRACTICE\\AI-based-job-application-portal-master\\mysite\\media\\jobs\\pdfs"

    @staticmethod
    def get_latest_resume():
        # Retrieve the most recent resume file from the specified directory
        resumes = [os.path.join(Details.resume_dir, f) for f in os.listdir(Details.resume_dir)]
        if not resumes:
            return None  # No resumes found
        latest_resume = max(resumes, key=os.path.getmtime)
        return latest_resume

    def get_queryset(self):
        # Get the latest resume path
        resume_path = self.get_latest_resume()
        print(f"Resume path: {resume_path}")
        if not resume_path:
            print(f"NO Resume")
            return []  # No resume to process

        # Extract text from the resume
        text = extract_text_from_pdf(resume_path)

        # Define the skill list
        skills_list = ['Python', 'Data Analysis', 'Machine Learning','SpringBoot', 'Communication', 'Project Management', 'Deep Learning', 'SQL', 'Tableau',
    'Java', 'C++', 'JavaScript', 'HTML', 'CSS', 'React', 'Angular', 'Node.js', 'MongoDB', 'Express.js', 'Git',
    'Research', 'Statistics', 'Quantitative Analysis', 'Qualitative Analysis', 'SPSS', 'R', 'Data Visualization', 'Matplotlib',
    'Seaborn', 'Plotly', 'Pandas', 'Numpy', 'Scikit-learn', 'TensorFlow', 'Keras', 'PyTorch', 'NLTK', 'Text Mining',
    'Natural Language Processing', 'Computer Vision', 'Image Processing', 'OCR', 'Speech Recognition', 'Recommendation Systems',
    'Collaborative Filtering', 'Content-Based Filtering', 'Reinforcement Learning', 'Neural Networks', 'Convolutional Neural Networks',
    'Recurrent Neural Networks', 'Generative Adversarial Networks', 'XGBoost', 'Random Forest', 'Decision Trees', 'Support Vector Machines',
    'Linear Regression', 'Logistic Regression', 'K-Means Clustering', 'Hierarchical Clustering', 'DBSCAN', 'Association Rule Learning',
    'Apache Hadoop', 'Apache Spark', 'MapReduce', 'Hive', 'HBase', 'Apache Kafka', 'Data Warehousing', 'ETL', 'Big Data Analytics',
    'Cloud Computing', 'Amazon Web Services (AWS)', 'Microsoft Azure', 'Google Cloud Platform (GCP)', 'Docker', 'Kubernetes', 'Linux',
    'Shell Scripting', 'Cybersecurity', 'Network Security', 'Penetration Testing', 'Firewalls', 'Encryption', 'Malware Analysis',
    'Digital Forensics', 'CI/CD', 'DevOps', 'Agile Methodology', 'Scrum', 'Kanban', 'Continuous Integration', 'Continuous Deployment',
    'Software Development', 'Web Development', 'Mobile Development', 'Backend Development', 'Frontend Development', 'Full-Stack Development',
    'UI/UX Design', 'Responsive Design', 'Wireframing', 'Prototyping', 'User Testing', 'Adobe Creative Suite', 'Photoshop', 'Illustrator',
    'InDesign', 'Figma', 'Sketch', 'Zeplin', 'InVision', 'Product Management', 'Market Research', 'Customer Development', 'Lean Startup',
    'Business Development', 'Sales', 'Marketing', 'Content Marketing', 'Social Media Marketing', 'Email Marketing', 'SEO', 'SEM', 'PPC',
    'Google Analytics', 'Facebook Ads', 'LinkedIn Ads', 'Lead Generation', 'Customer Relationship Management (CRM)', 'Salesforce',
    'HubSpot', 'Zendesk', 'Intercom', 'Customer Support', 'Technical Support', 'Troubleshooting', 'Ticketing Systems', 'ServiceNow',
    'ITIL', 'Quality Assurance', 'Manual Testing', 'Automated Testing', 'Selenium', 'JUnit', 'Load Testing', 'Performance Testing',
    'Regression Testing', 'Black Box Testing', 'White Box Testing', 'API Testing', 'Mobile Testing', 'Usability Testing', 'Accessibility Testing',
    'Cross-Browser Testing', 'Agile Testing', 'User Acceptance Testing', 'Software Documentation', 'Technical Writing', 'Copywriting',
    'Editing', 'Proofreading', 'Content Management Systems (CMS)', 'WordPress', 'Joomla', 'Drupal', 'Magento', 'Shopify', 'E-commerce',
    'Payment Gateways', 'Inventory Management', 'Supply Chain Management', 'Logistics', 'Procurement', 'ERP Systems', 'SAP', 'Oracle',
    'Microsoft Dynamics', 'Tableau', 'Power BI', 'QlikView', 'Looker', 'Data Warehousing', 'ETL', 'Data Engineering', 'Data Governance',
    'Data Quality', 'Master Data Management', 'Predictive Analytics', 'Prescriptive Analytics', 'Descriptive Analytics', 'Business Intelligence',
    'Dashboarding', 'Reporting', 'Data Mining', 'Web Scraping', 'API Integration', 'RESTful APIs', 'GraphQL', 'SOAP', 'Microservices',
    'Serverless Architecture', 'Lambda Functions', 'Event-Driven Architecture', 'Message Queues', 'GraphQL', 'Socket.io', 'WebSockets'
'Ruby', 'Ruby on Rails', 'PHP', 'Symfony', 'Laravel', 'CakePHP', 'Zend Framework', 'ASP.NET', 'C#', 'VB.NET', 'ASP.NET MVC', 'Entity Framework',
    'Spring', 'Hibernate', 'Struts', 'Kotlin', 'Swift', 'Objective-C', 'iOS Development', 'Android Development', 'Flutter', 'React Native', 'Ionic',
    'Mobile UI/UX Design', 'Material Design', 'SwiftUI', 'RxJava', 'RxSwift', 'Django', 'Flask', 'FastAPI', 'Falcon', 'Tornado', 'WebSockets',
    'GraphQL', 'RESTful Web Services', 'SOAP', 'Microservices Architecture', 'Serverless Computing', 'AWS Lambda', 'Google Cloud Functions',
    'Azure Functions', 'Server Administration', 'System Administration', 'Network Administration', 'Database Administration', 'MySQL', 'PostgreSQL',
    'SQLite', 'Microsoft SQL Server', 'Oracle Database', 'NoSQL', 'MongoDB', 'Cassandra', 'Redis', 'Elasticsearch', 'Firebase', 'Google Analytics',
    'Google Tag Manager', 'Adobe Analytics', 'Marketing Automation', 'Customer Data Platforms', 'Segment', 'Salesforce Marketing Cloud', 'HubSpot CRM',
    'Zapier', 'IFTTT', 'Workflow Automation', 'Robotic Process Automation (RPA)', 'UI Automation', 'Natural Language Generation (NLG)',
    'Virtual Reality (VR)', 'Augmented Reality (AR)', 'Mixed Reality (MR)', 'Unity', 'Unreal Engine', '3D Modeling', 'Animation', 'Motion Graphics',
    'Game Design', 'Game Development', 'Level Design', 'Unity3D', 'Unreal Engine 4', 'Blender', 'Maya', 'Adobe After Effects', 'Adobe Premiere Pro',
    'Final Cut Pro', 'Video Editing', 'Audio Editing', 'Sound Design', 'Music Production', 'Digital Marketing', 'Content Strategy', 'Conversion Rate Optimization (CRO)',
    'A/B Testing', 'Customer Experience (CX)', 'User Experience (UX)', 'User Interface (UI)', 'Persona Development', 'User Journey Mapping', 'Information Architecture (IA)',
    'Wireframing', 'Prototyping', 'Usability Testing', 'Accessibility Compliance', 'Internationalization (I18n)', 'Localization (L10n)', 'Voice User Interface (VUI)',
    'Chatbots', 'Natural Language Understanding (NLU)', 'Speech Synthesis', 'Emotion Detection', 'Sentiment Analysis', 'Image Recognition', 'Object Detection',
    'Facial Recognition', 'Gesture Recognition', 'Document Recognition', 'Fraud Detection', 'Cyber Threat Intelligence', 'Security Information and Event Management (SIEM)',
    'Vulnerability Assessment', 'Incident Response', 'Forensic Analysis', 'Security Operations Center (SOC)', 'Identity and Access Management (IAM)', 'Single Sign-On (SSO)',
    'Multi-Factor Authentication (MFA)', 'Blockchain', 'Cryptocurrency', 'Decentralized Finance (DeFi)', 'Smart Contracts', 'Web3', 'Non-Fungible Tokens (NFTs)']
  # (shortened for brevity)

        # Extract applicant details
        global name, phone, email, skills
        name = extract_name(text)
        phone = extract_mobile_number(text)
        email = extract_email(text)
        skills = extract_skills(text, skills_list)

        # Retrieve job based on job_id parameter
        job_id = self.kwargs.get("job_id")
        print(f"jobID: {job_id}")
       #id=job_id
        job = get_object_or_404(Job,id=job_id)

        # Get matching skills for the specified job  job_id
        matching_skills = get_matching_skills(skills,job_id)

        # Print extracted information for debugging
        print(f"Name: {name}")
        print(f"Phone: {phone}")
        print(f"Email: {email}")
        print(f"Skills: {skills}")
        print(f"Matching Skills: {matching_skills}")

        # Save applicant details
        details = Applicant(resume=resume_path, name=name, phone=phone, email=email, matching_skills=matching_skills)
        details.save()

        for obj in Applicant.objects.all():
            if(not obj.name):
                obj.delete()

        return Applicant.objects.all()
    
#def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
 #       context['job_id'] = self.kwargs['job_id']  # Get job_id from URL pattern
#        return context

class Questions(generic.CreateView):
    model = answer
    form_class = Question_Form
    template_name = 'jobs/questions.html'
    success_url = reverse_lazy('final')


class answerValidate(generic.ListView):
    template_name = 'jobs/final.html'

    def get_queryset(self):
        # Correcting the list comprehension syntax
        ans = [x.answer1 for x in answer.objects.all()] + \
              [x.answer2 for x in answer.objects.all()] + \
              [x.answer3 for x in answer.objects.all()] + \
              [x.answer4 for x in answer.objects.all()] + \
              [x.answer5 for x in answer.objects.all()]

        result = function(ans)
        result = round(sum(result) / len(result), 2)

        # Retrieve the designation for the job
        designation = Job.objects.first().Designation if Job.objects.exists() else None

        # Save final result details
        final_data = Result(Designation=designation, name=name, phone=phone, email=email, skills=skills, score=result)
        final_data.save()

        return [final_data]

