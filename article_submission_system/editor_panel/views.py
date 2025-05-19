# editor_panel/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from admin_panel.models import UserProfile, Article, Category 
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

def editor_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('editor_dashboard')  # Redirect to the dashboard after login
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'editor_panel/E_TEMP/editor_login.html')  # Render the login template

@login_required
def editor_logout(request):
    logout(request)
    return redirect('editor_login')  # Redirect to the login page after logout


@login_required
def editor_dashboard(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    submitted_articles = Article.objects.filter(assigned_to=user_profile)
    categories = Category.objects.filter(editors=request.user)
    categories = Category.objects.all()  # Fetch all categories
# Debugging output
    print("Submitted Articles:", submitted_articles)
    print("Categories:", categories)  # This should show the categories

    return render(request, 'editor_panel/E_TEMP/editor_dashboard.html', {
        'submitted_articles': submitted_articles,
        'categories': categories,  # Pass categories to the template
    })

def editor_profile(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        
        user = user_profile.user
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        
        user.save()
        
        messages.success(request, "User  details updated successfully.")
        return redirect('editor_dashboard')
    
    return render(request, 'editor_panel/E_TEMP/editor_profile.html', {'user_profile': user_profile})

@login_required
def draft(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    submitted_articles = Article.objects.filter(assigned_to=user_profile)
    categories = Category.objects.all()  # Fetch all categories
# Debugging output
    print("Submitted Articles:", submitted_articles)
    print("Categories:", categories)

    return render(request, 'editor_panel/E_TEMP/articles.html', {
        'submitted_articles': submitted_articles,
        'categories': categories,  # Pass categories to the template
    })
    



@login_required
def submit_article(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        category_id = request.POST['category']
        
        # Ensure the category exists
        category = get_object_or_404(Category, id=category_id)

        # Create and save the article
        article = Article(
            title=title,
            content=content,
            category=category,
            status='pending',
            assigned_to=request.user.userprofile  # Ensure this is correct
        )
        article.save()
        messages.success(request, "Article submitted successfully.")
        return redirect('editor_dashboard')  # Ensure this matches the URL pattern name

    return render(request, 'editor_panel/E_TEMP/submit_article.html')  # Updated path

@login_required
def view_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    return render(request, 'editor_panel/E_TEMP/view_article.html', {'article': article})  # Updated path

@login_required
def edit_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    if request.method == 'POST':
        article.title = request.POST['title']
        article.content = request.POST['content']
        article.category_id = request.POST['category']  # Update the category
        article.status = 'pending'  # Reset status to pending after editing
        article.save()
        messages.success(request, "Article updated successfully.")
        return redirect('editor_dashboard')  # Ensure this matches the URL pattern name

    categories = Category.objects.all()  # Get all categories for the dropdown
    return render(request, 'editor_panel/E_TEMP/edit_article.html', {  # Updated path
        'article': article,
        'categories': categories,
    })

@login_required
def resubmit_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    if request.method == 'POST':
        article.title = request.POST['title']
        article.content = request.POST['content']
        article.status = 'pending'
        article.save()
        messages.success(request, "Article resubmitted successfully.")
        return redirect('editor_dashboard')  # Ensure this matches the URL pattern name
    return render(request, 'editor_panel/E_TEMP/resubmit_article.html', {'article': article})  # Updated path