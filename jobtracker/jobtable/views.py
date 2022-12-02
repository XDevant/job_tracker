from django.shortcuts import render, redirect
from django.db.models import F, ExpressionWrapper, CharField
from . import forms
from .models import Prospect


def jobs(request):
    prospects = Prospect.objects.all()
    prospects = sorted(prospects,
                       key=lambda obj: obj.date_updated if obj.date_updated else obj.date_created,
                       reverse=True)
    for prospect in prospects:
        prospect.site_name = prospect.website.split('//')[-1].split('/')[0]
    context = {'prospects': prospects}
    return render(request, 'jobtable/home.html', context=context)


def create_prospect(request):
    if request.method == 'POST':
        prospect_form = forms.ProspectForm(request.POST)
        if prospect_form.is_valid():
            prospect = prospect_form.save(commit=False)
            prospect.save()
            return redirect('jobs')
    context = {'form': forms.ProspectForm}
    return render(request, 'jobtable/create_prospect.html', context=context)
