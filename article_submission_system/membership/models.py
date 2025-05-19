# membership/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser 

class MembershipRequest(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    country = models.CharField(max_length=100)  # Corrected from 'county' to 'country'
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False) 
    role_assigned = models.BooleanField(default=False) 
    published = models.BooleanField(default=False)  # New field to indicate if the article is published
    published_at = models.DateTimeField(null=True, blank=True)  # Timestamp for when the article is published


    def __str__(self):
        return self.full_name


class CustomUser (AbstractUser ):
    email = models.EmailField(unique=True)

    # Specify related_name to avoid clashes
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Change this to a unique name
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  # Change this to a unique name
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.email