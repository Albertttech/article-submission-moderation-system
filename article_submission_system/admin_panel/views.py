# admin_panel/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import UserProfile, Category, Article
from django.contrib.auth.models import User
from django.contrib import messages
from membership.models import MembershipRequest 
import random
import string

def team_login(request):
    return render(request, 'team_login.html') 

def moderator_login(request):
    return render(request, 'moderator_login.html')

def editor_login(request):
    return render(request, 'editor_login.html')  

def admin_dashboard(request):
    users = UserProfile.objects.all()
    return render(request, 'admin_panel/dashboard.html', {'users': users})

def home(request):
    return redirect('admin_dashboard')  # Redirect to the admin dashboard

def add_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        work_id = request.POST['work_id']
        role = request.POST['role']
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('add_user')
        
        if UserProfile.objects.filter(user__username=username, role=role).exists():
            messages.error(request, f"A user with the username '{username}' already exists as a {role}.")
            return redirect('add_user')
        
        user = User.objects.create_user(username=username, password=password)
        UserProfile.objects.create(user=user, role=role, work_id=work_id)
        messages.success(request, "User  added successfully.")
        return redirect('admin_dashboard')
    
    return render(request, 'admin_panel/add_user.html')

def edit_user(request, user_id):
    user_profile = get_object_or_404(UserProfile, id=user_id)
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        work_id = request.POST['work_id']
        role = request.POST['role']
        
        user = user_profile.user
        user.username = username
        user.work_id = work_id
        if password:
            user.set_password(password)
        
        user.save()
        user_profile.role = role
        user_profile.save()
        
        messages.success(request, "User  details updated successfully.")
        return redirect('admin_dashboard')
    
    return render(request, 'admin_panel/edit_user.html', {'user_profile': user_profile})
def message_user(request, user_id):
    #users = get_object_or_404(UserProfile, id=user_id)
    user_profile = get_object_or_404(UserProfile, id=user_id)
    return render(request, 'admin_panel/message_user.html', {'user_profile': user_profile})

def delete_user(request, user_id):
    user_profile = get_object_or_404(UserProfile, id=user_id)
    user_profile.user.delete()
    user_profile.delete()
    messages.success(request, "User  deleted successfully.")
    return redirect('admin_dashboard')

def add_category(request):
    if request.method == 'POST':
        name = request.POST['name']
        
        if Category.objects.filter(name=name).exists():
            messages.error(request, "Category with this name already exists.")
            return redirect('add_category')
        
        Category.objects.create(name=name)
        messages.success(request, "Category added successfully.")
        return redirect('category_management')
    
    return render(request, 'admin_panel/add_category.html')

def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    
    if request.method == 'POST':
        category.name = request.POST['name']
        category.save()
        messages.success(request, "Category updated successfully.")
        return redirect('category_management')
    
    return render(request, 'admin_panel/edit_category.html', {'category': category})

def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    messages.success(request, "Category deleted successfully.")
    return redirect('category_management')

def category_management(request):
    categories = Category.objects.all()
    return render(request, 'admin_panel/category_management.html', {'categories': categories})

def submission_statistics(request):
    total_submissions = Article.objects.count()
    approved_submissions = Article.objects.filter(status='approved').count()
    return render(request, 'admin_panel/submission_statistics.html', {
        'total_submissions': total_submissions,
        'approved_submissions': approved_submissions,
    })

def reporting_view(request):
    total_submissions = Article.objects.count()
    approved_submissions = Article.objects.filter(status='approved').count()
    rejected_submissions = Article.objects.filter(status='rejected').count()
    approval_rate = (approved_submissions / total_submissions * 100) if total_submissions > 0 else 0
    submissions_per_category = Article.objects.values('category__name').annotate(count=models.Count('id'))

    context = {
        'total_submissions': total_submissions,
        'approved_submissions': approved_submissions,
        'rejected_submissions': rejected_submissions,
        'approval_rate': approval_rate,
        'submissions_per_category': submissions_per_category,
    }
    return render(request, 'admin_panel/reporting.html', context)

def approve_membership(request, request_id):
    membership_request = get_object_or_404(MembershipRequest, id=request_id)
    membership_request.is_approved = True  # Set the is_approved field to True
    membership_request.save()  # Save the changes
    messages.success(request, "Membership request approved successfully.")
    return redirect('admin_dashboard')  # Redirect to the admin dashboard

def delete_membership_request(request, request_id):
    membership_request = get_object_or_404(MembershipRequest, id=request_id)
    membership_request.delete()  # Delete the membership request
    messages.success(request, "Membership request deleted successfully.")
    return redirect('admin_dashboard')  # Redirect to the admin dashboard


def admin_dashboard(request):
    users = UserProfile.objects.all()  # Fetch all user profiles
    # Fetch only membership requests that are approved but not assigned a role
    #membership_requests = MembershipRequest.objects.filter(is_approved=True, role_assigned=False)
    membership_requests = MembershipRequest.objects.all()
    return render(request, 'admin_panel/dashboard.html', {
        'users': users,
        'membership_requests': membership_requests,  # Pass membership requests to the template
    })

def assign_role(request, request_id):
    membership_request = get_object_or_404(MembershipRequest, id=request_id)

    if request.method == 'POST':
        username = request.POST['username']  # This will be left blank
        password = request.POST['password']
        role = request.POST['role']
        work_id = request.POST['work_id']  # New field for Work ID

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('assign_role', request_id=request_id)

        user = User.objects.create_user(username=username, password=password)
        UserProfile.objects.create(user=user, role=role, work_id=work_id)  # Create the user profile

        # Update the membership request to indicate that a role has been assigned
        membership_request.role_assigned = True
        membership_request.save()

        messages.success(request, "User  added successfully.")
        return redirect('admin_dashboard')

    return render(request, 'admin_panel/add_user.html', {
        'username': '',  # Leave username blank
        'work_id': '',   # Placeholder for Work ID
        'full_name': membership_request.full_name,  # Display the full name
    })