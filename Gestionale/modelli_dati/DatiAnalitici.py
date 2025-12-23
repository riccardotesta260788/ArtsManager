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


class Iscrizioni(models.Model):
    history = AuditlogHistoryField()
    # Dati analitici dell'opera

    classe_appartenenza = models.TextField(default='', blank=True, null=True,
                                           help_text='Es. Celebrativa, commemorativa....')
    lingua = models.CharField(max_length=100, default='', blank=True, null=True, help_text='')
    tecnica_scrittura = models.CharField(max_length=100, default='', blank=True, null=True, help_text='')
    tipo_caratteri = models.CharField(max_length=100, default='', blank=True, null=True, help_text='')
    posizione = models.CharField(max_length=100, default='', blank=True, null=True, help_text='')
    autore = models.CharField(max_length=100, default='', blank=True, null=True, help_text='')
    trascrizione = models.CharField(max_length=100, default='', blank=True, null=True, help_text='')

    # Strutture accessorie
    # nome del record collegato alla vista del modello
    def __str__(self):
        # return self.posizione_archivio+" - "+self.autore.cognome+" - "+self.titolo_opera+" / "+self.anno_realizzazione.__str__()
        abs = '>| '.join([str(self.lingua), self.trascrizione, ])
        return abs

    class Meta:
        verbose_name_plural = "Iscrizioni"


class DatiAnalitici(models.Model):
    history = AuditlogHistoryField()
    # Dati analitici dell'opera

    iscrizioni = models.ManyToManyField(Iscrizioni, default='', blank=True, null=True)

    # Strutture accessorie
    # nome del record collegato alla vista del modello
    def __str__(self):
        # return self.posizione_archivio+" - "+self.autore.cognome+" - "+self.titolo_opera+" / "+self.anno_realizzazione.__str__()
        abs = ' - '.join([str(self.id), self.descrizione, ])
        return abs

    class Meta:
        verbose_name_plural = "Dati analitici"
