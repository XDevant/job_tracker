from django.contrib import admin
from .models import Prospect, Candidature, Contact, Letter


class ProspectAdmin(admin.ModelAdmin):
    list_display = ('job', 'company', 'source', 'post_url', 'website', 'email')
    ordering = ('date_created', )


admin.site.register(Prospect, ProspectAdmin)
admin.site.register(Candidature)
admin.site.register(Contact)
admin.site.register(Letter)
