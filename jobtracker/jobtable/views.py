from django.shortcuts import render, redirect
from . import forms


def jobs(request):
    context = {}
    return render(request, 'jobtable/home.html', context=context)


def create_prospect(request):
    if request.method == 'POST':
        prospect_form = forms.ProspectForm(request.POST)
        if prospect_form.is_valid():
            prospect = prospect_form.save(commit=False)
            prospect.user = request.user
            prospect.save()
            return redirect('jobs')
    context = {'form': forms.ProspectForm}
    return render(request, 'jobtable/create_prospect.html', context=context)
