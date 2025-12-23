from django.db import models as models
from Gestionale import models as modelli
from django.db.models.signals import post_init
import time
from django.core.validators import int_list_validator
from django.contrib.postgres.fields import ArrayField
from Gestionale.models import Opera
from jsonfield import JSONField


class ImageColorFeatures(models.Model):
    image = models.ForeignKey(Opera, on_delete=models.DO_NOTHING)
    real_color = models.TextField(null=True, blank=True)
    named_color = models.TextField(null=True, blank=True)

    def __str__(self):
        return "{} - {} ".format(self.image.autore, self.image.titolo_opera)


class GlobalColorFeatures(models.Model):
    real_color = JSONField(null=True)
    named_color = JSONField(null=True)
