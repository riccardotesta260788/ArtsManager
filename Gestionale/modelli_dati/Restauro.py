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


class Restauro(models.Model):
    history = AuditlogHistoryField()
    # Indicazioni sul restauro
    data = models.DateField(blank=True, null=True)
    situazione = models.CharField(max_length=300, default='', blank=True, null=True, help_text='Stato dell\'opera')
    ente_responsabile = models.CharField(max_length=100, default='', blank=True, null=True, help_text='')
    operatore = models.CharField(max_length=100, default='', blank=True, null=True, help_text='')
    ente_responsabile = models.CharField(max_length=100, default='', blank=True, null=True, help_text='')

    # Strutture accessorie
    # nome del record collegato alla vista del modello
    def __str__(self):
        # return self.posizione_archivio+" - "+self.autore.cognome+" - "+self.titolo_opera+" / "+self.anno_realizzazione.__str__()
        abs = '-'.join([str(self.data), self.ente_responsabile, ])
        return abs

    class Meta:
        verbose_name_plural = "Restauri"
