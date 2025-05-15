from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class Project(models.Model):
    CATEGORY_CHOICES = [
        ('web', 'Web Development'),
        ('mobile', 'Mobile Development'),
        ('ai', 'AI/ML'),
        ('cloud', 'Cloud Solutions'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to='projects/')
    github_url = models.URLField(blank=True)
    live_url = models.URLField(blank=True)
    technologies = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    featured = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_created']
        indexes = [
            models.Index(fields=['-date_created']),
            models.Index(fields=['category']),
        ]

    def __str__(self):
        return self.title

class Skill(models.Model):
    SKILL_CATEGORIES = [
        ('backend', 'Backend'),
        ('frontend', 'Frontend'),
        ('database', 'Database'),
        ('devops', 'DevOps'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=100)
    proficiency = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        help_text="Proficiency percentage (1-100)"
    )
    category = models.CharField(max_length=20, choices=SKILL_CATEGORIES)
    order = models.PositiveIntegerField(default=0)
    show_in_chart = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', '-proficiency']

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"

class ContactRequest(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new'
    )
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Request'
        verbose_name_plural = 'Contact Requests'

    def __str__(self):
        return f"Contact from {self.name} - {self.created_at.strftime('%Y-%m-%d')}"