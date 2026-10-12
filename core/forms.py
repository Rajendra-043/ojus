from django import forms
from .models import Feedback, Registration


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ["name", "email", "phone", "club", "event", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Enter name"}),
            "email": forms.EmailInput(attrs={"placeholder": "Enter email"}),
            "phone": forms.TextInput(attrs={"placeholder": "Enter phone"}),
            "message": forms.Textarea(attrs={"placeholder": "Write your query"}),
        }


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ["name", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Your name"}),
            "message": forms.Textarea(attrs={"placeholder": "Write your feedback"}),
        }
