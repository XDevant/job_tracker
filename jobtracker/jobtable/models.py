from django.db import models
from django.conf import settings
from .fixtures.letters import cover_template


class Contact(models.Model):
    user = models.ForeignKey(
                             to=settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='contact_user'
                             )
    email = models.EmailField(max_length=64, unique=True)
    name = models.CharField(max_length=64, null=True)
    tel = models.IntegerField(null=True)
    linkedin = models.URLField(max_length=64, null=True)
    comments = models.TextField(max_length=300, null=True)

    def __str__(self):
        return self.email


class Prospect(models.Model):
    class Sizes(models.TextChoices):
        NA = "Inconnue"
        MICRO = "1-5"
        MINI = "6-20"
        SMALL = "21-50"
        MEDIUM = "51-250"
        BIG = "251-1000"
        GIANT = "1000+"

    contacts = models.ManyToManyField(to=Contact, through='Insider')
    company = models.CharField(max_length=64)
    activity = models.CharField(max_length=64, null=True)
    size = models.CharField(max_length=16, default=Sizes.NA, choices=Sizes.choices)
    localisation = models.CharField(max_length=64, null=True, default=None)
    website = models.URLField(max_length=64, null=True)
    email = models.EmailField(max_length=64)
    comments = models.TextField(max_length=300, null=True)
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(default=None, null=True)
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return self.company


class Insider(models.Model):
    prospect = models.ForeignKey(to=Prospect,
                                 on_delete=models.CASCADE,
                                 related_name='contact_prospect',
                                 )
    contact = models.ForeignKey(to=Contact,
                                on_delete=models.CASCADE,
                                related_name='prospect_contact',
                                )

    class Meta:
        unique_together = ('prospect', 'contact',)


class Mail(models.Model):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='mail_user'
    )
    contact = models.ForeignKey(
        to=Contact,
        on_delete=models.CASCADE,
        related_name='mail_contact',
    )
    greet = models.CharField(max_length=64, default=cover_template["greet"])
    you = models.TextField(max_length=450, default=cover_template["you"], null=True)
    me = models.TextField(max_length=450, default=cover_template["me"], null=True)
    us = models.TextField(max_length=450, default=cover_template["us"], null=True)
    salute = models.CharField(max_length=64, default=cover_template["salute"], null=True)
    date = models.CharField(max_length=64, default="12 décembre 2022", null=True)
    is_mail = models.BooleanField(default=True)
    sent = models.BooleanField(default=True)
    date_sent = models.DateField(default=None, null=True)


class Application(models.Model):
    class Type(models.TextChoices):
        FULL_CDI = 'CDI Temps plein'
        FULL_CDD = 'CDD Temps plein'
        PARTIAL_CDI = 'CDI Temps partiel'
        PARTIAL_CDD = 'CDD Temps partiel'
        STAGE = 'Stage'

    class Result(models.TextChoices):
        OK = 'OK'
        KO = 'KO'
        NY = 'En attente'
        AR = 'A recontacter'

    class Source(models.TextChoices):
        LinkedIn = 'LinkedIn'
        Indeed = 'Indeed'
        Pole_Emploi = 'Pôle emploi'
        Apec = 'Apec'
        Other = 'Autre'
        Unknown = 'Spontanée'

    user = models.ForeignKey(
                             to=settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='application_user',
                            )
    prospect = models.ForeignKey(to=Prospect,
                                 on_delete=models.CASCADE,
                                 related_name='application_prospect',
                                 )
    mails = models.ManyToManyField(to=Mail, through='Exchange')
    job = models.CharField(max_length=64, null=True)
    type = models.CharField(max_length=18, default=Type.FULL_CDI, choices=Type.choices)
    source = models.CharField(max_length=16, choices=Source.choices, default=Source.Unknown)
    source_url = models.URLField(max_length=128, null=True)
    date_interview = models.DateField(default=None, null=True)
    comments = models.TextField(max_length=500, default=None, null=True)
    notes = models.TextField(max_length=500, default=None, null=True)
    result = models.CharField(choices=Result.choices, max_length=16)
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(default=None, null=True)
    is_archived = models.BooleanField(default=False)


class Exchange(models.Model):
    application = models.ForeignKey(
                                    to=Application,
                                    on_delete=models.CASCADE,
                                    related_name='mail_application',
                                    )
    mail = models.ForeignKey(
                             to=Mail,
                             on_delete=models.CASCADE,
                             related_name='application_mail',
                             )
