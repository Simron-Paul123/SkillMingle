# Generated by Django 5.1.2 on 2024-10-27 07:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('icon_class', models.CharField(help_text="CSS class for icon, e.g., 'ri-pencil-ruler-2-fill'", max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('location', models.CharField(max_length=100)),
                ('job_type', models.CharField(max_length=50)),
                ('image_url', models.URLField(blank=True, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jobs', to='skill.category')),
            ],
        ),
    ]
