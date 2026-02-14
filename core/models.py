from django.db import models
from django.utils.text import slugify


class SiteSettings(models.Model):
    """Singleton model for site-wide settings."""
    name = models.CharField(max_length=100, help_text="Your full name")
    title = models.CharField(max_length=200, help_text="e.g., Full Stack Developer")
    bio = models.TextField(help_text="About you paragraph")
    photo_url = models.URLField(blank=True, help_text="URL to your profile photo")
    email = models.EmailField()
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    resume_url = models.URLField(blank=True, help_text="Link to your resume/CV")

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return f"Settings for {self.name}"

    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and SiteSettings.objects.exists():
            existing = SiteSettings.objects.first()
            self.pk = existing.pk
        super().save(*args, **kwargs)

    @classmethod
    def get_settings(cls):
        """Get or create the singleton settings instance."""
        settings, created = cls.objects.get_or_create(
            pk=1,
            defaults={
                'name': 'Mohamed Ali Hussien',
                'title': 'Full Stack Developer',
                'bio': 'Passionate developer creating modern web applications.',
                'email': 'contact@example.com',
            }
        )
        return settings


class Skill(models.Model):
    """Skills and technologies."""
    CATEGORY_CHOICES = [
        ('frontend', 'Frontend'),
        ('backend', 'Backend'),
        ('tools', 'Tools & DevOps'),
        ('database', 'Database'),
    ]

    name = models.CharField(max_length=50)
    icon = models.CharField(max_length=50, help_text="Font Awesome class, e.g., 'fa-python'")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    proficiency = models.IntegerField(default=80, help_text="1-100 proficiency level")
    display_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'name']

    def __str__(self):
        return self.name


class Project(models.Model):
    """Portfolio projects."""
    CATEGORY_CHOICES = [
        ('website', 'Website'),
        ('django_app', 'Django Application'),
        ('api', 'API / Backend'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    tagline = models.CharField(max_length=200, help_text="Short one-liner description")
    description = models.TextField(help_text="Full project description")
    thumbnail = models.URLField(help_text="URL to project thumbnail image")
    screenshots = models.JSONField(
        default=list,
        blank=True,
        help_text="List of screenshot URLs as JSON array"
    )
    live_url = models.URLField(help_text="Live demo URL")
    github_url = models.URLField(blank=True, help_text="GitHub repository URL")
    tech_stack = models.JSONField(
        default=list,
        help_text="List of technologies, e.g., [\"Django\", \"PostgreSQL\"]"
    )
    features = models.JSONField(
        default=list,
        help_text="List of key features"
    )
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='website')
    is_featured = models.BooleanField(default=False, help_text="Show prominently on homepage")
    display_order = models.IntegerField(default=0, help_text="Lower numbers appear first")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', '-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class ContactInquiry(models.Model):
    """Contact form submissions."""
    INQUIRY_CHOICES = [
        ('general', 'General Inquiry'),
        ('project', 'Project Inquiry'),
    ]

    BUDGET_CHOICES = [
        ('under_1k', 'Under $1,000'),
        ('1k_5k', '$1,000 - $5,000'),
        ('5k_10k', '$5,000 - $10,000'),
        ('over_10k', 'Over $10,000'),
        ('discuss', 'Let\'s Discuss'),
    ]

    TIMELINE_CHOICES = [
        ('asap', 'ASAP'),
        ('1_month', 'Within 1 month'),
        ('1_3_months', '1-3 months'),
        ('3_plus_months', '3+ months'),
        ('flexible', 'Flexible'),
    ]

    inquiry_type = models.CharField(max_length=20, choices=INQUIRY_CHOICES, default='general')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

    # Project-specific fields
    budget = models.CharField(max_length=20, choices=BUDGET_CHOICES, blank=True)
    timeline = models.CharField(max_length=20, choices=TIMELINE_CHOICES, blank=True)
    project_description = models.TextField(blank=True, help_text="Detailed project requirements")

    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Contact Inquiry"
        verbose_name_plural = "Contact Inquiries"

    def __str__(self):
        return f"{self.inquiry_type.title()} from {self.name}"
