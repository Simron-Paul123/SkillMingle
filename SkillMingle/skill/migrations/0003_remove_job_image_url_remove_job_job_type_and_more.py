# Generated by Django 5.0.3 on 2024-10-27 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('skill', '0002_remove_category_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='image_url',
        ),
        migrations.RemoveField(
            model_name='job',
            name='job_type',
        ),
        migrations.AddField(
            model_name='job',
            name='company_logo',
            field=models.ImageField(default='company_logos/default.png', upload_to='company_logos/'),
        ),
        migrations.AddField(
            model_name='job',
            name='company_name',
            field=models.CharField(default='Default Company Name', max_length=100),
        ),
        migrations.AddField(
            model_name='job',
            name='employment_type',
            field=models.CharField(default='Full Time', max_length=50),
        ),
        migrations.AddField(
            model_name='job',
            name='positions',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='job',
            name='salary',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='job',
            name='description',
            field=models.TextField(default='Job Description not provided.'),
        ),
        migrations.AlterField(
            model_name='job',
            name='location',
            field=models.CharField(default='Unknown Location', max_length=100),
        ),
        migrations.AlterField(
            model_name='job',
            name='title',
            field=models.CharField(default='Job Title', max_length=100),
        ),
    ]
