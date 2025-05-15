from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q
from .models import Project, Skill, ContactRequest
from .forms import ContactForm, ProjectForm, SkillForm

def home(request):
    featured_projects = Project.objects.filter(featured=True)[:3]
    skills = Skill.objects.filter(show_in_chart=True).order_by('-proficiency')

    backend_skills = skills.filter(category='backend')
    frontend_skills = skills.filter(category='frontend')
    database_skills = skills.filter(category='database')
    tools_skills = skills.filter(category='tools')

    context = {
        'featured_projects': featured_projects,
        'backend_skills': backend_skills,
        'frontend_skills': frontend_skills,
        'database_skills': database_skills,
        'tools_skills': tools_skills,
    }

    return render(request, 'index.html', context)



class ProjectListView(ListView):
    model = Project
    template_name = 'projects.html'
    context_object_name = 'projects'
    paginate_by = 6
    ordering = ['-date_created']

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.GET.get('category')
        search = self.request.GET.get('q')

        if category:
            queryset = queryset.filter(category=category)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(technologies__icontains=search)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Project.CATEGORY_CHOICES
        return context

class ProjectDetailView(DetailView):
    model = Project
    template_name = 'project_detail.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()
        related_projects = Project.objects.filter(
            category=project.category
        ).exclude(pk=project.pk)[:3]
        context['related_projects'] = related_projects
        return context

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_request = form.save(commit=False)
            
            # Add request metadata
            contact_request.ip_address = request.META.get('REMOTE_ADDR')
            contact_request.user_agent = request.META.get('HTTP_USER_AGENT', '')[:255]
            contact_request.save()

            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})

def about(request):
    skills = Skill.objects.all().order_by('category', '-proficiency')
    return render(request, 'about.html', {'skills': skills})

# Admin Views
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project created successfully!')
            return redirect('projects')
    else:
        form = ProjectForm()
    return render(request, 'create_project.html', {'form': form})

def manage_skills(request):
    skills = Skill.objects.all().order_by('order')
    
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill added successfully!')
            return redirect('manage_skills')
    else:
        form = SkillForm()

    context = {
        'skills': skills,
        'form': form
    }
    return render(request, 'manage_skills.html', context)

