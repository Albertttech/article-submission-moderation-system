# editor_panel/models.py

from django.db import models
from admin_panel.models import Article, UserProfile, Category
from django.contrib.auth.models import User



class Draft(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='drafts')  # Added related_name for clarity
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Draft for {self.article.title}"


class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    assigned_to = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='editor_articles')  # Added related_name
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, related_name='editor_articles')  # Added related_name

    def __str__(self):
        return self.title