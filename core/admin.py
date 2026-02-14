from django.contrib import admin
from .models import SiteSettings, Skill, Project, ContactInquiry


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'email']

    def has_add_permission(self, request):
        # Only allow one instance
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'proficiency', 'display_order']
    list_filter = ['category']
    list_editable = ['proficiency', 'display_order']
    ordering = ['display_order', 'name']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'is_featured', 'display_order', 'created_at']
    list_filter = ['category', 'is_featured']
    list_editable = ['is_featured', 'display_order']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'description', 'tagline']
    ordering = ['display_order', '-created_at']

    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'slug', 'tagline', 'description', 'category')
        }),
        ('Media', {
            'fields': ('thumbnail', 'screenshots')
        }),
        ('Links', {
            'fields': ('live_url', 'github_url')
        }),
        ('Details', {
            'fields': ('tech_stack', 'features')
        }),
        ('Display', {
            'fields': ('is_featured', 'display_order')
        }),
    )


@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'inquiry_type', 'is_read', 'created_at']
    list_filter = ['inquiry_type', 'is_read', 'created_at']
    list_editable = ['is_read']
    search_fields = ['name', 'email', 'message']
    readonly_fields = ['created_at']
    ordering = ['-created_at']

    fieldsets = (
        ('Contact Info', {
            'fields': ('name', 'email', 'inquiry_type')
        }),
        ('Message', {
            'fields': ('message',)
        }),
        ('Project Details', {
            'fields': ('budget', 'timeline', 'project_description'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_read', 'created_at')
        }),
    )
