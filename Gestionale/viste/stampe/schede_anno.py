from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from Gestionale.models import *

'''Estrazione delle elenco completo delle opere e autori con descrizione'''


@login_required
def opere_anno_list_full(request, year):
    entry = Opera.objects.filter(edizione__contains=year, tag__contains="finalista").order_by('posizione_archivio')
    return render(request, 'reports/brochure_edizione_completa.html', context={"anno_edizione": year, "entries": entry})
