# membership/views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import MembershipRequestForm
from .models import MembershipRequest

def team_login(request):
    return render(request, 'team_login.html')

def request_membership(request):
    if request.method == 'POST':
        form = MembershipRequestForm(request.POST)

        # Check if the form is valid before accessing cleaned_data
        if form.is_valid():
            # Check if the email already exists in the MembershipRequest model
            if MembershipRequest.objects.filter(email=form.cleaned_data.get('email')).exists():
                messages.error(request, "A membership request with this email already exists.")
                return render(request, 'membership/request_membership.html', {'form': form})

            form.save()  # Save the membership request
            messages.success(request, "Your membership request has been submitted successfully.")
            return redirect('membership:success')  # Redirect to the success page
    else:
        form = MembershipRequestForm()
    
    return render(request, 'membership/request_membership.html', {'form': form})

def success_page(request):
    return render(request, 'membership/success.html')

def member_list(request):
    members = MembershipRequest.objects.filter(is_approved=True)  # Get only approved members
    return render(request, 'membership/member_list.html', {'members': members})