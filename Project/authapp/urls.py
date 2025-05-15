from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Main Application URLs
    path('', views.home, name='home'),
    path('projects/', views.ProjectListView.as_view(), name='projects'),
    path('projects/<slug:slug>/', views.ProjectDetailView.as_view(), name='project_detail'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    
    # Admin Management URLs
    path('admin/create-project/', views.create_project, name='create_project'),
    path('admin/manage-skills/', views.manage_skills, name='manage_skills'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)