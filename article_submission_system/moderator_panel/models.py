# moderator_panel/models.py

from django.db import models
from admin_panel.models import Article, UserProfile  # Import necessary models

class ModerationAction(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    moderator = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    action = models.CharField(max_length=20, choices=[
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('revision requested', 'Revision Requested'),
    ])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} by {self.moderator} on {self.article.title}"