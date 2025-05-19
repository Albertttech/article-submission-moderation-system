# moderator_panel/views.py

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from admin_panel.models import UserProfile, Article, Notification
from django.utils import timezone

@login_required
def moderator_dashboard(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    articles = Article.objects.filter(assigned_to=user_profile)
    return render(request, 'moderator_panel/moderator_dashboard.html', {'articles': articles})

def moderator_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.userprofile.role == 'moderator':
            login(request, user)
            return redirect('moderator_dashboard')
        else:
            messages.error(request, "Invalid username or password, or you do not have moderator access.")
    
    return render(request, 'moderator_panel/moderator_login.html')

def moderator_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('moderator_login')

@login_required
def view_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    return render(request, 'moderator_panel/view_article.html', {'article': article})

def approve_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    if article.status in ['approved', 'rejected', 'revision requested']:
        messages.error(request, "This article has already been processed. No further actions can be taken.")
        return redirect('moderator_dashboard')

    article.status = 'approved'
    article.save()
    messages.success(request, "Article approved successfully.")
    return redirect('moderator_dashboard')

def reject_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    if article.status in ['approved', 'rejected', 'revision requested']:
        messages.error(request, "This article has already been processed. No further actions can be taken.")
        return redirect('moderator_dashboard')

    article.status = 'rejected'
    article.save()
    
    # Create a notification for the editor
    Notification.objects.create(user=article.assigned_to.user, message=f"Your article '{article.title}' has been rejected.")
    
    messages.success(request, "Article rejected successfully.")
    return redirect('moderator_dashboard')

def request_revision(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    if article.status in ['approved', 'rejected', 'revision requested']:
        messages.error(request, "This article has already been processed. No further actions can be taken.")
        return redirect('moderator_dashboard')

    if request.method == 'POST':
        comment = request.POST.get('comment', '')
        article.status = 'revision requested'
        article.revision_comment = comment  # Assuming you have a field for this
        article.save()
        messages.success(request, "Revision requested successfully.")
        return redirect('moderator_dashboard')
    
    return render(request, 'moderator_panel/request_revision.html', {'article': article})



@login_required
def publish_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    if article.status != 'approved':
        messages.error(request, "Only approved articles can be published.")
        return redirect('moderator_dashboard')

    article.published = True
    article.published_at = timezone.now()  # Set the current time as the published time
    article.save()

    messages.success(request, "Article published successfully.")
    return redirect('moderator_dashboard')