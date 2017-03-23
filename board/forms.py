from django import forms
from django.contrib.auth.models import User
from .models import Note, Project


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']


class NoteForm(forms.ModelForm):

    class Meta:
        model = Note
        fields = ['task', 'group', 'description', 'tags']
        
class ProjectForm(forms.ModelForm):
    
    class Meta:
        model = Project
        fields = ['project']