# membership/forms.py

from django import forms
from .models import MembershipRequest

class MembershipRequestForm(forms.ModelForm):
    class Meta:
        model = MembershipRequest
        fields = ['full_name', 'email', 'country']  # Corrected 'county' to 'country'