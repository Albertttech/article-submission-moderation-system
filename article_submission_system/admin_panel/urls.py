# admin_panel/urls.py

from django.urls import path
from membership.views import request_membership
from .views import (
    admin_dashboard,
    add_user,
    edit_user,
    message_user,
    delete_user,
    category_management,
    add_category,
    edit_category,
    delete_category,
    submission_statistics,
    reporting_view,
    team_login,
    approve_membership,
    delete_membership_request,
    assign_role,
)

urlpatterns = [
    path('', admin_dashboard, name='admin_dashboard'),
    path('team/', team_login, name='team_login'), 
    path('request_membership/', request_membership, name='request_membership'),
    path('approve_membership/<int:request_id>/', approve_membership, name='approve_membership'),
    path('delete_membership_request/<int:request_id>/', delete_membership_request, name='delete_membership_request'), 
    path('assign_role/<int:request_id>/', assign_role, name='assign_role'),

    path('add_user/', add_user, name='add_user'),
    path('edit_user/<int:user_id>/', edit_user, name='edit_user'),
    path('message_user/<int:user_id>/', message_user, name='message_user'),
    path('delete_user/<int:user_id>/', delete_user, name='delete_user'),

    path('categories/', category_management, name='category_management'),
    path('add_category/', add_category, name='add_category'),  
    path('edit_category/<int:category_id>/', edit_category, name='edit_category'),  
    path('delete_category/<int:category_id>/', delete_category, name='delete_category'),  
    path('submission_statistics/', submission_statistics, name='submission_statistics'), 
    path('reporting/', reporting_view, name='reporting'),
]