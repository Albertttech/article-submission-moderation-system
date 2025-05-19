# membership/urls.py

from django.urls import path
from .views import request_membership, success_page, member_list  # Import all necessary views

app_name = 'membership'

urlpatterns = [
    path('request/', request_membership, name='request_membership'),  # URL for requesting membership
    path('success/', success_page, name='success'),  # URL for the success page
    path('members/', member_list, name='member_list'),  # URL for the member list
]