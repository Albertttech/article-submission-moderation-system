# public/urls.py

from django.urls import path
from .views import published_articles, view_article

urlpatterns = [
    path('articles/', published_articles, name='published_articles'),
    path('view_article/<int:article_id>/', view_article, name='view_article'),  # Define the URL pattern
    
]