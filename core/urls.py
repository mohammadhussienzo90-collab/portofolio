from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('project/<slug:slug>/', views.project_detail, name='project_detail'),
    path('contact/', views.contact_submit, name='contact_submit'),
    path('seed-data/', views.seed_data, name='seed_data'),
]
