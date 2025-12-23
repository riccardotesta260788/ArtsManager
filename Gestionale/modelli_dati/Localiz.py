import datetime
import os
import urllib
from collections import OrderedDict
from io import BytesIO

import PIL
from django.conf import settings
from django.db import models
from django.utils.safestring import mark_safe
from phonenumber_field.modelfields import PhoneNumberField

from django.db import models

from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog

tipologia = (('AR', 'AR - Archivio'), ('RA', 'RA - Raccolta'))


class Localizzazione(models.Model):
    history = AuditlogHistoryField()
    # Localizzaizone dell'opera
    stato = models.CharField(max_length=400, default='', blank=True, null=True)
    regione = models.TextField(default='', blank=True, null=True)
    provincia = models.CharField(max_length=60, default='', blank=True, null=True)
    comune = models.CharField(max_length=60, default='', blank=True, null=True)

    # Strutture accessorie
    # nome del record collegato alla vista del modello
    def __str__(self):
        # return self.posizione_archivio+" - "+self.autore.cognome+" - "+self.titolo_opera+" / "+self.anno_realizzazione.__str__()
        abs = '-'.join([self.comune, self.stato])
        return abs

    class Meta:
        verbose_name_plural = "Localizzazioni"


class LocalizzazioneSpecifica(models.Model):
    history = AuditlogHistoryField()
    # Localizzaizone dell'opera
    localizzazione = models.ForeignKey(Localizzazione, on_delete=models.DO_NOTHING, related_name='localizzazione',
                                       blank=True, )
    tipologia = models.CharField(choices=tipologia, max_length=30, default='', blank=True, null=True)
    denominazione = models.TextField(default='', blank=True, null=True)
    spazio_viabilistico = models.CharField(max_length=60, default='', blank=True, null=True)
    denominazione_raccolta = models.CharField(max_length=60, default='', blank=True, null=True)
    specifiche = models.CharField(max_length=150, default='', blank=True, null=True)

    # Strutture accessorie
    # nome del record collegato alla vista del modello
    def __str__(self):
        # return self.posizione_archivio+" - "+self.autore.cognome+" - "+self.titolo_opera+" / "+self.anno_realizzazione.__str__()
        abs = '-'.join([self.denominazione, self.localizzazione.__str__(), " > ", self.specifiche, ])
        return abs

    class Meta:
        verbose_name_plural = "Localizzazioni Specifiche"
