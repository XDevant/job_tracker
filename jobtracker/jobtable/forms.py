from django import forms
from . import models
from django.forms.widgets import Textarea


class ProspectForm(forms.ModelForm):
    """Model form, title translation and custom imagefield widget"""
    class Meta:
        model = models.Prospect
        fields = ('company', 'activity', 'size', 'website', 'email', 'comments')
        labels = {'company': 'Entreprise',
                  'activity': 'Activité',
                  'size': 'Employés',
                  'website': 'Site Web',
                  'email': 'Couriel',
                  'comments': 'Notes',
                  }
        widgets = {}
