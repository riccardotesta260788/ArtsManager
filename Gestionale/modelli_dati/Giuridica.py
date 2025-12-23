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


class Giuridica(models.Model):
    history = AuditlogHistoryField()
    # Indicazioni sul restauro
    indicazione_generica = models.CharField(max_length=100, default='', blank=True, null=True, help_text='')
    indicazione_specifica = models.CharField(max_length=100, default='', blank=True, null=True, help_text='')
    indirizzo = models.CharField(max_length=100, default='', blank=True, null=True, help_text='')
    tipo_provvedimento_tutela = models.CharField(max_length=100, default='', blank=True, null=True, help_text='')
    estremi_provvedimento_tutela = models.CharField(max_length=100, default='', blank=True, null=True, help_text='')
    data_notifica_provvedimento = models.DateField(default='', blank=True, null=True, help_text='')

    # Strutture accessorie
    # nome del record collegato alla vista del modello
    def __str__(self):
        # return self.posizione_archivio+" - "+self.autore.cognome+" - "+self.titolo_opera+" / "+self.anno_realizzazione.__str__()
        abs = '-'.join([str(self.indicazione_generica)])
        return abs

    class Meta:
        verbose_name_plural = "Giuridica"
