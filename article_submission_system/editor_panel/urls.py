# editor_panel/urls.py

from django.urls import path
from .views import (
    editor_profile,
    editor_dashboard,
    submit_article,
    view_article as editor_view_article,  # Rename the view for clarity 
    resubmit_article,
    edit_article,
    editor_login,
    editor_logout,
    draft,
)

urlpatterns = [
    path('profile/', editor_profile, name='editor_profile'),
    path('articles/', draft, name='draft'),
    path('dashboard/', editor_dashboard, name='editor_dashboard'),
    path('submit/', submit_article, name='submit_article'),
    path('view/<int:article_id>/', editor_view_article, name='editor_view_article'),  # Renamed for clarity
    path('resubmit/<int:article_id>/', resubmit_article, name='resubmit_article'),
    path('login/', editor_login, name='editor_login'),  # Ensure this line is present
    path('logout/', editor_logout, name='editor_logout'),
    path('edit/<int:article_id>/', edit_article, name='edit_article'),
]