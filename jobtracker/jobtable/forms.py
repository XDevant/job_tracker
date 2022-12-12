from django import forms
from . import models
from django.forms.widgets import Textarea


class ProspectForm(forms.ModelForm):
    """Model form, title translation and custom imagefield widget"""
    class Meta:
        model = models.Prospect
        fields = ('company', 'activity', 'localisation', 'size', 'website', 'email', 'comments')
        labels = {'company': 'Entreprise',
                  'activity': 'Activité',
                  'localisation': 'Lieu',
                  'size': 'Employés',
                  'website': 'Site Web',
                  'email': 'Couriel',
                  'comments': 'Notes',
                  }
        widgets = {}


class ApplicationForm(forms.ModelForm):
    """Model form with title translation for model application"""
    class Meta:
        model = models.Application
        fields = ('prospect', 'job', 'source', 'source_url', 'type', 'comments')
        labels = {
                  'prospect': 'Entreprise',
                  'job': 'Poste',
                  'source': 'Source',
                  'source_url': 'URL source',
                  'type': 'Type de contrat',
                  'comments': 'Commentaire'
                 }


class MailboxForm(forms.Form):
    cover = forms.BooleanField(initial=False)
    cv = forms.BooleanField(initial=False)

    class Meta:
        labels = {
                  'cover': 'Lettre de motivation',
                  'cv': 'CV'
                  }
