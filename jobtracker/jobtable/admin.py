from django.contrib import admin
from .models import Prospect, Application, Contact, Mail, Insider, Exchange


class ProspectAdmin(admin.ModelAdmin):
    list_display = ('company', 'activity', 'size', 'website', 'email', 'comments')
    ordering = ('date_created', )


admin.site.register(Prospect, ProspectAdmin)
admin.site.register(Application)
admin.site.register(Contact)
admin.site.register(Insider)
admin.site.register(Mail)
admin.site.register(Exchange)