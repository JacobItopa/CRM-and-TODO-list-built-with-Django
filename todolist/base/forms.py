from dataclasses import fields
from pyexpat import model
from django import forms
from .models import task
from django.contrib.auth.forms import UserCreationForm

class TaskModelForm(forms.ModelForm):
    class Meta:
        model = task
        fields = (
            'title',
            'description',
            'complete',
            
        )

class CustomUserCreationForm(UserCreationForm):
    pass
