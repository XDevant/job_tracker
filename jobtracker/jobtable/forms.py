from django import forms
from . import models
from django.forms.widgets import Textarea


class ProspectForm(forms.ModelForm):
    """Model form, title translation and custom imagefield widget"""
    class Meta:
        model = models.Prospect
        fields = ('job', 'company', 'source', 'post_url', 'website', 'email')
        labels = {'job': 'Poste',
                  'company': 'Entreprise',
                  'source': 'Source',
                  'post_url': 'Annonce',
                  'website': 'Site Web',
                  'email': 'Couriel',
                  }
        widgets = {}
