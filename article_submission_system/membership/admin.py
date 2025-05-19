# membership/admin.py

from django.contrib import admin
from .models import MembershipRequest

@admin.register(MembershipRequest)
class MembershipRequestAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'county', 'created_at', 'is_approved')
    search_fields = ('full_name', 'email')