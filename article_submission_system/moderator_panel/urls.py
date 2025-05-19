# moderator_panel/urls.py

from django.urls import path
from .views import (  # Import views from the same app
    moderator_dashboard,
    approve_article,
    reject_article,
    request_revision,
    moderator_login,
    moderator_logout,
    view_article as moderator_view_article,  # Rename the view for clarity
    publish_article,
)

urlpatterns = [
    path('dashboard/', moderator_dashboard, name='moderator_dashboard'),
    path('approve/<int:article_id>/', approve_article, name='approve_article'),
    path('reject/<int:article_id>/', reject_article, name='reject_article'),
    path('request_revision/<int:article_id>/', request_revision, name='request_revision'),
    path('login/', moderator_login, name='moderator_login'),
    path('logout/', moderator_logout, name='moderator_logout'),
    path('view/<int:article_id>/', moderator_view_article, name='moderator_view_article'),  # Renamed for clarity
    path('publish_article/<int:article_id>/', publish_article, name='publish_article'),
]