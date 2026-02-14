from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from .models import Project, Skill, SiteSettings, ContactInquiry
from .forms import ContactForm, ProjectInquiryForm


def home(request):
    """Home page with all portfolio sections."""
    settings = SiteSettings.get_settings()
    projects = Project.objects.all()
    featured_projects = projects.filter(is_featured=True)
    skills = Skill.objects.all()

    # Group skills by category
    skills_by_category = {}
    for skill in skills:
        category = skill.get_category_display()
        if category not in skills_by_category:
            skills_by_category[category] = []
        skills_by_category[category].append(skill)

    context = {
        'settings': settings,
        'projects': projects,
        'featured_projects': featured_projects,
        'skills': skills,
        'skills_by_category': skills_by_category,
        'contact_form': ContactForm(),
        'project_form': ProjectInquiryForm(),
    }
    return render(request, 'home.html', context)


def project_detail(request, slug):
    """Individual project detail page."""
    project = get_object_or_404(Project, slug=slug)
    settings = SiteSettings.get_settings()

    # Get related projects (same category, excluding current)
    related_projects = Project.objects.filter(
        category=project.category
    ).exclude(pk=project.pk)[:3]

    context = {
        'project': project,
        'settings': settings,
        'related_projects': related_projects,
    }
    return render(request, 'project_detail.html', context)


@require_POST
@csrf_protect
def contact_submit(request):
    """Handle contact form submission via AJAX."""
    form_type = request.POST.get('form_type', 'general')

    if form_type == 'project':
        form = ProjectInquiryForm(request.POST)
    else:
        form = ContactForm(request.POST)

    if form.is_valid():
        form.save()
        return JsonResponse({
            'success': True,
            'message': 'Thank you for your message! I\'ll get back to you soon.'
        })
    else:
        return JsonResponse({
            'success': False,
            'errors': form.errors
        }, status=400)


def seed_data(request):
    """Seed initial data for the portfolio."""
    # Create site settings if not exists
    settings = SiteSettings.get_settings()
    settings.name = "Mohamed Ali Hussien"
    settings.title = "Full Stack Developer"
    settings.bio = """Passionate Full Stack Developer with expertise in Django, Python, and modern web technologies.
    I build scalable web applications that solve real-world problems. Currently focused on creating
    exceptional digital experiences that combine clean code with beautiful design."""
    settings.email = "mohammadhussienzo90@gmail.com"
    settings.github_url = "https://github.com/mohammadhussienzo90-collab"
    settings.save()

    # Create skills
    skills_data = [
        {'name': 'Python', 'icon': 'fab fa-python', 'category': 'backend', 'proficiency': 95},
        {'name': 'Django', 'icon': 'fas fa-cube', 'category': 'backend', 'proficiency': 90},
        {'name': 'JavaScript', 'icon': 'fab fa-js', 'category': 'frontend', 'proficiency': 85},
        {'name': 'HTML/CSS', 'icon': 'fab fa-html5', 'category': 'frontend', 'proficiency': 90},
        {'name': 'PostgreSQL', 'icon': 'fas fa-database', 'category': 'database', 'proficiency': 85},
        {'name': 'SQLite', 'icon': 'fas fa-database', 'category': 'database', 'proficiency': 90},
        {'name': 'Git', 'icon': 'fab fa-git-alt', 'category': 'tools', 'proficiency': 90},
        {'name': 'Docker', 'icon': 'fab fa-docker', 'category': 'tools', 'proficiency': 75},
        {'name': 'REST APIs', 'icon': 'fas fa-plug', 'category': 'backend', 'proficiency': 90},
        {'name': 'Tailwind CSS', 'icon': 'fas fa-wind', 'category': 'frontend', 'proficiency': 85},
    ]

    for i, skill_data in enumerate(skills_data):
        Skill.objects.update_or_create(
            name=skill_data['name'],
            defaults={**skill_data, 'display_order': i}
        )

    # Create Egy360 project
    Project.objects.update_or_create(
        slug='egy360',
        defaults={
            'title': 'Egy360',
            'tagline': 'Discover Egypt - A comprehensive tourism and travel platform',
            'description': """Egy360 is a full-featured tourism platform showcasing Egypt's rich heritage,
            from ancient pyramids to modern attractions. Built with Django, it features an elegant UI,
            comprehensive destination guides, tour booking capabilities, and a dynamic content management system.

            The platform includes interactive maps, curated travel itineraries, hotel recommendations,
            and detailed articles about Egyptian history and culture. Designed with both tourists and
            travel agencies in mind, Egy360 provides a seamless experience for planning the perfect Egyptian adventure.""",
            'thumbnail': 'https://images.unsplash.com/photo-1539768942893-daf53e448371?w=800',
            'screenshots': [
                'https://images.unsplash.com/photo-1539768942893-daf53e448371?w=1200',
                'https://images.unsplash.com/photo-1553913861-c0fddf2619ee?w=1200',
                'https://images.unsplash.com/photo-1568322445389-f64ac2515020?w=1200',
            ],
            'live_url': 'https://egy360.up.railway.app',
            'github_url': 'https://github.com/mohammadhussienzo90-collab/Egy360',
            'tech_stack': ['Django', 'Python', 'SQLite', 'Tailwind CSS', 'Alpine.js', 'Railway'],
            'features': [
                'Dynamic destination guides with rich media',
                'Interactive tour booking system',
                'Curated hotel recommendations',
                'Comprehensive article management',
                'Responsive, mobile-first design',
                'SEO optimized content',
                'Admin dashboard for content management',
            ],
            'category': 'website',
            'is_featured': True,
            'display_order': 1,
        }
    )

    return JsonResponse({'success': True, 'message': 'Data seeded successfully!'})
