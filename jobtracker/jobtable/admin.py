from django.contrib import admin
from .models import Prospect, Candidature, Contact, Letter


class ProspectAdmin(admin.ModelAdmin):
    list_display = ('company', 'activity', 'size', 'website', 'email', 'comments')
    ordering = ('date_created', )


admin.site.register(Prospect, ProspectAdmin)
admin.site.register(Candidature)
admin.site.register(Contact)
admin.site.register(Letter)
