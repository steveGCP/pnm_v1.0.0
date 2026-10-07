from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        #On n'affiche que les champs que l'utilisateur doit remplir
        fields = ['name', 'pitch']
