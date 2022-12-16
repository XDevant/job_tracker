from django.contrib import admin
from .models import Prospect, Application, Contact, Mail, Insider, Exchange


class ProspectAdmin(admin.ModelAdmin):
    list_display = ('company', 'activity', 'size', 'website', 'email', 'comments')
    ordering = ('date_created', )


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('prospect', 'job', 'type', 'source', 'comments', 'notes', 'result')
    ordering = ('date_created', )


class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'tel', 'linkedin', 'comments')
    ordering = ('name', )


class InsiderAdmin(admin.ModelAdmin):
    list_display = ('contact', 'prospect')
    ordering = ('prospect',)


class MailAdmin(admin.ModelAdmin):
    list_display = ('contact', 'greet', 'you', 'me', 'us', 'salute', 'date', 'is_mail', 'sent', 'date_sent')
    ordering = ('contact', 'date_sent')


class ExchangeAdmin(admin.ModelAdmin):
    list_display = ('mail', 'application')
    ordering = ('application',)


admin.site.register(Prospect, ProspectAdmin)
admin.site.register(Application, ApplicationAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Insider, InsiderAdmin)
admin.site.register(Mail, MailAdmin)
admin.site.register(Exchange, ExchangeAdmin)
