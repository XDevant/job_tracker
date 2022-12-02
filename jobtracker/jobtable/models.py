from django.db import models
from django.conf import settings


class Prospect(models.Model):
    job = models.CharField(max_length=64)
    company = models.CharField(max_length=64)
    source = models.CharField(max_length=12, null=True)
    post_url = models.URLField(max_length=64, null=True)
    website = models.URLField(max_length=64, null=True)
    email = models.EmailField(max_length=64)
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(default=None, null=True)
    date_archived = models.DateField(default=None, null=True)


class Candidature(models.Model):
    class Result(models.TextChoices):
        OK = 'OK'
        KO = 'KO'
        NY = 'En attente'
        AR = 'A recontacter'

    user = models.ForeignKey(
                             to=settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='candidature_user',
                            )
    prospect = models.ForeignKey(to=Prospect,
                                 on_delete=models.CASCADE,
                                 related_name='candidature_prospect',
                                 )
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(default=None)
    date_envoi = models.DateField(default=None)
    relances = models.IntegerField(default=0)
    date_relance = models.DateField(default=None)
    date_entretien = models.DateField(default=None)
    comments = models.TextField(max_length=300)
    result = models.CharField(choices=Result.choices, max_length=16)


class Contact(models.Model):
    user = models.ForeignKey(
                             to=settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='contact_user'
                             )
    name = models.CharField(max_length=64)
    email = models.EmailField(max_length=64)
    tel = models.IntegerField()
    linkedin = models.URLField(max_length=64)
    comments = models.TextField(max_length=300)


class Letter(models.Model):
    user = models.ForeignKey(
                             to=settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='letter_user'
                             )
    candidature = models.ForeignKey(to=Candidature,
                                    on_delete=models.CASCADE,
                                    related_name='letter_candidature')
    you = models.TextField(max_length=300)
    me = models.TextField(max_length=300)
    us = models.TextField(max_length=300)
