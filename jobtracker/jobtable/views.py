from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import EmailMessage
from django.urls import reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from . import forms
from .models import Prospect, Application, Mail, Contact, Insider, Exchange


@login_required
def jobs(request):
    prospects = Prospect.objects.all()
    prospects = sorted(prospects,
                       key=lambda obj: obj.date_updated if obj.date_updated else obj.date_created,
                       reverse=True)
    for prospect in prospects:
        prospect.site_name = prospect.website.split('//')[-1].split('/')[0]
    context = {'prospects': prospects}
    return render(request, 'jobtable/home.html', context=context)


@login_required
def list_prospects(request):
    prospects = Prospect.objects.all()
    prospects = sorted(prospects,
                       key=lambda obj: obj.date_updated if obj.date_updated else obj.date_created,
                       reverse=True)
    for prospect in prospects:
        prospect.site_name = prospect.website.split('//')[-1].split('/')[0]
    context = {'prospects': prospects,
               'actions': True}
    return render(request, 'jobtable/list_prospects.html', context=context)


def detail_prospect(request, pk):
    try:
        prospect = Prospect.objects.get(id=pk)
        contact_list = Insider.objects.filter(prospect=prospect)
    except ObjectDoesNotExist:
        return redirect('list-prospects')
    context = {'prospect': prospect,
               'contact_list': contact_list}
    return render(request, 'jobtable/prospect_detail.html', context=context)


@login_required
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
    Args: request object
         Int positive, pk
    Return: String (HTML)
    """
    try:
        prospect = Prospect.objects.get(id=pk)
    except ObjectDoesNotExist:
        return redirect('list-prospects')
    if request.method == 'POST':
        prospect.objects.delete()
        return redirect('list-prospects')
    return render(request, 'jobtable/confirm_delete.html', {'item': prospect, 'type': 'prospect'})


class ApplicationListView(ListView):
    model = Application


class ApplicationDetailView(DetailView):
    model = Application

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        application = get_object_or_404(Application, id=self.kwargs['pk'])
        contact_list = Insider.objects.filter(prospect=application.prospect)
        context['contact_list'] = contact_list
        mail_list = Exchange.objects.filter(application=application)
        context['mail_list'] = mail_list
        return context


class ApplicationCreateView(CreateView):
    model = Application
    fields = ['prospect', 'job', 'source', 'source_url', 'type', 'comments']
    pk = None

    def post(self, request):
        form = self.get_form()
        if form.is_valid():
            form.instance.user = self.request.user
            application = form.save()
            self.pk = application.id
            return redirect('application-detail', pk=self.pk)
        return render(request, 'jobtable/application_form.html', {'form': form})

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('application-detail', kwargs={'pk': self.pk})


class ApplicationUpdateView(UpdateView):
    model = Application
    fields = ['name']
    template_name_suffix = '_update_form'


class ApplicationDeleteView(UpdateView):
    model = Application


class ContactListView(ListView):
    model = Contact


class ContactCreateView(CreateView):
    model = Contact
    fields = ['email', 'name', 'tel', 'linkedin', 'comments']

    def post(self, request, pk):
        form = self.get_form()
        if form.is_valid():
            form.instance.user = self.request.user
            contact = form.save()
            prospect = Prospect.objects.get(id=pk)
            Insider.objects.create(contact=contact, prospect=prospect)
            return redirect('prospect-detail', pk=pk)
        return render(request, 'jobtable/contact_form.html', {'form': form})

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class MailListView(ListView):
    model = Mail


class MailCreateView(CreateView):
    model = Mail
    fields = ['contact', 'greet', 'you', 'me', 'us', 'salute', 'is_mail', 'sent']

    def post(self, request, pk):
        form = self.get_form()
        if form.is_valid():
            form.instance.user = self.request.user
            mail = form.save()
            application = Application.objects.get(id=pk)
            Exchange.objects.create(application=application, mail=mail)
            return redirect('application-detail', pk=pk)
        return render(request, 'jobtable/mail_form.html', {'form': form})

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class LetterDetailView(DetailView):
    model = Exchange


class MailboxView(FormView):
    form_class = forms.MailboxForm
    template_name = 'jobtable/email.html'
    pk = None

    def post(self, request, pk):
        form = self.get_form()
        exchange = get_object_or_404(Exchange, id=pk)
        self.pk = exchange.application.id
        body = exchange.mail.greet + '\n' + exchange.mail.you + '\n' + exchange.mail.me + '\n' + exchange.mail.us
        body += exchange.mail.salute + '\n' + exchange.mail.user.email
        email = EmailMessage(
            subject=exchange.application.job,
            body=body,
            from_email=exchange.mail.user.email,
            to=(exchange.mail.contact.email,),
        )
        # if form.is_valid():
            # email.attach_file()
        email.send(fail_silently=False)

    def get_success_url(self):
        return reverse('application-detail', kwargs={'pk': self.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        exchange = Exchange.objects.get(id=self.kwargs['pk'])
        context['exchange'] = exchange
        return context
