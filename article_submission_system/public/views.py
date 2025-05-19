# public/views.py 

from django.shortcuts import render, get_object_or_404
from admin_panel.models import Article

def published_articles(request):
    # Order articles by published_at in descending order
    articles = Article.objects.filter(published=True).order_by('-published_at')
    return render(request, 'public/published_articles.html', {'articles': articles})

def view_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    return render(request, 'public/view_article.html', {'article': article})