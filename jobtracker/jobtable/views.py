from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
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


def lists_prospects(request):
    prospects = Prospect.objects.all()
    prospects = sorted(prospects,
                       key=lambda obj: obj.date_updated if obj.date_updated else obj.date_created,
                       reverse=True)
    for prospect in prospects:
        prospect.site_name = prospect.website.split('//')[-1].split('/')[0]
    context = {'prospects': prospects}
    return render(request, 'jobtable/list_prospects.html', context=context)


def create_prospect(request):
    if request.method == 'POST':
        prospect_form = forms.ProspectForm(request.POST)
        if prospect_form.is_valid():
            prospect = prospect_form.save(commit=False)
            prospect.save()
            return redirect('list-prospects')
    context = {'form': forms.ProspectForm}
    return render(request, 'jobtable/create_prospect.html', context=context)


@login_required
def edit_prospect(request, pk):
    """
    Arg: request object
         Int positive, id
    Return: String (HTML)
    """
    try:
        prospect = Prospect.objects.get(id=pk)
    except ObjectDoesNotExist:
        return redirect('list-prospects')
    if request.method == 'POST':
        form = forms.ProspectForm(request.POST, instance=prospect)
        if form.is_valid():
            form.save()
            return redirect('list-prospects')
    else:
        form = forms.ProspectForm(instance=prospect)
    return render(request, 'jobtable/edit_prospect.html', {'form': form})


@login_required
def delete_prospect(request, pk):
    """
    Arg: request object
         Int positive, id
    Return: String (HTML)
    """
    try:
        prospect = Prospect.objects.get(id=pk)
    except ObjectDoesNotExist:
        return redirect('list-prospects')
    if request.method == 'POST':
        return redirect('list-prospects')
    return render(request, 'jobtable/delete_prospect.html', {'prospect': prospect})
