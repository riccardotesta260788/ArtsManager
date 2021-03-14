import itertools

from django.shortcuts import render
from django.http import HttpResponse
import datetime
from django.template.loader import get_template

from Gestionale.models import *
from django.http import JsonResponse


def get_eta(request):
    anni = [0,25, 35, 50, 60, 80]
    autors=[]
    today = datetime.date.today()
    format = "%Y-%m-%d"

    deltime = [(today - datetime.timedelta(days=anno * 365)).strftime(format) for anno in anni]
    # deltime.insert(0,today.strftime(format))
    list_cycle = itertools.cycle(deltime)
    next(list_cycle)
    print(deltime)
    for index,interval in enumerate(deltime):
        if index<len(deltime)-1:
            upperval=str(next(list_cycle))
            lowerval=str(interval)
            value=Autore.objects.filter(nascita__gt=upperval, nascita__lt=lowerval).count()
            print(index,value,lowerval, upperval)
            autors.append(value)

    value = Autore.objects.filter(nascita__lt=deltime[-1]).count()
    print(len(deltime)-1,value, deltime[-1])
    autors.append(value)

    print(Autore.objects.filter(nascita__gt='1970-01-01').all().count())
    print(autors)

    anni_cycle = itertools.cycle(anni)
    next(anni_cycle)

    labels=['%s-%s'% (str(cicle), str(next(anni_cycle))) for index,cicle in enumerate(anni) if index<len(anni)-1 ]
    labels.append('+%s'%anni[-1])

    contesto = {"dataresult": autors, "labels": labels}

    return JsonResponse(contesto)
