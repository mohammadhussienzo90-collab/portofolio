# Generated migration for Portfolio core app

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContactInquiry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inquiry_type', models.CharField(choices=[('general', 'General Inquiry'), ('project', 'Project Inquiry')], default='general', max_length=20)),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('message', models.TextField()),
                ('budget', models.CharField(blank=True, choices=[('under_1k', 'Under $1,000'), ('1k_5k', '$1,000 - $5,000'), ('5k_10k', '$5,000 - $10,000'), ('over_10k', 'Over $10,000'), ('discuss', "Let's Discuss")], max_length=20)),
                ('timeline', models.CharField(blank=True, choices=[('asap', 'ASAP'), ('1_month', 'Within 1 month'), ('1_3_months', '1-3 months'), ('3_plus_months', '3+ months'), ('flexible', 'Flexible')], max_length=20)),
                ('project_description', models.TextField(blank=True, help_text='Detailed project requirements')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_read', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Contact Inquiry',
                'verbose_name_plural': 'Contact Inquiries',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('tagline', models.CharField(help_text='Short one-liner description', max_length=200)),
                ('description', models.TextField(help_text='Full project description')),
                ('thumbnail', models.URLField(help_text='URL to project thumbnail image')),
                ('screenshots', models.JSONField(blank=True, default=list, help_text='List of screenshot URLs as JSON array')),
                ('live_url', models.URLField(help_text='Live demo URL')),
                ('github_url', models.URLField(blank=True, help_text='GitHub repository URL')),
                ('tech_stack', models.JSONField(default=list, help_text='List of technologies, e.g., ["Django", "PostgreSQL"]')),
                ('features', models.JSONField(default=list, help_text='List of key features')),
                ('category', models.CharField(choices=[('website', 'Website'), ('django_app', 'Django Application'), ('api', 'API / Backend'), ('other', 'Other')], default='website', max_length=20)),
                ('is_featured', models.BooleanField(default=False, help_text='Show prominently on homepage')),
                ('display_order', models.IntegerField(default=0, help_text='Lower numbers appear first')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['display_order', '-created_at'],
            },
        ),
        migrations.CreateModel(
            name='SiteSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Your full name', max_length=100)),
                ('title', models.CharField(help_text='e.g., Full Stack Developer', max_length=200)),
                ('bio', models.TextField(help_text='About you paragraph')),
                ('photo_url', models.URLField(blank=True, help_text='URL to your profile photo')),
                ('email', models.EmailField(max_length=254)),
                ('github_url', models.URLField(blank=True)),
                ('linkedin_url', models.URLField(blank=True)),
                ('resume_url', models.URLField(blank=True, help_text='Link to your resume/CV')),
            ],
            options={
                'verbose_name': 'Site Settings',
                'verbose_name_plural': 'Site Settings',
            },
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('icon', models.CharField(help_text="Font Awesome class, e.g., 'fa-python'", max_length=50)),
                ('category', models.CharField(choices=[('frontend', 'Frontend'), ('backend', 'Backend'), ('tools', 'Tools & DevOps'), ('database', 'Database')], max_length=20)),
                ('proficiency', models.IntegerField(default=80, help_text='1-100 proficiency level')),
                ('display_order', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['display_order', 'name'],
            },
        ),
    ]
