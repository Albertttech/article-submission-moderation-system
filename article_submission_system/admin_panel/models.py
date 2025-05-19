# admin_panel/models.py

from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('moderator', 'Moderator'),
        ('editor', 'Editor'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    work_id = models.CharField(max_length=9, blank=True, null=True)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=100)
    editors = models.ManyToManyField(User, related_name='categories', blank=True)  # Many-to-many relationship

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'), 
        ('approved', 'Approved'), 
        ('rejected', 'Rejected'),
        ('revision requested', 'Revision Requested')
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    assigned_to = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='admin_articles')  # Added related_name
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, related_name='admin_articles')  # Added related_name
    moderator_comment = models.TextField(blank=True, null=True) 
    role_assigned = models.BooleanField(default=False) 
    published = models.BooleanField(default=False)  # Indicates if the article is published
    published_at = models.DateTimeField(null=True, blank=True)  # Timestamp for when the article is published

    def __str__(self):
        return self.title

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message[:20]}..."  # Shortened message for display

class MembershipRequest(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    county = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    role_assigned = models.BooleanField(default=False)  # Indicates if a role has been assigned
    published = models.BooleanField(default=False)  # Indicates if the article is published
    published_at = models.DateTimeField(null=True, blank=True)  # Timestamp for when the article is published

    def __str__(self):
        return self.full_name