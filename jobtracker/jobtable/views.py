from django.shortcuts import render, redirect
from . import forms
from .models import Prospect


def jobs(request):
    prospects = sorted(Prospect.objects.all(),
                       key=lambda prospect: prospect.date_created,
                       reverse=True)
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
