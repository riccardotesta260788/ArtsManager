from django.shortcuts import render
from django.http import HttpResponse
import datetime
from django.template.loader import get_template
from django.http import HttpResponse
from .models import *
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'homepageNotLog.html', context={"message": "Home page"})


def login(request):
    return render(request, 'registration/login.html',context={})


def handler404(request):
    return render(request, 'errors.html', status=404, context={"errore": '404',
                                                               "message":"Pagina non trovata"})

def handler500(request):
    return render(request, 'errors.html', status=500,context={"errore":'500',
                                                              "message":"Errore del server"})

@login_required
def export_data_autori(request):
    entry=Opera.objects.all()
    return render(request, 'mainautori.html', context={"export_record":entry, "elementi":entry.count()})

@login_required
def export_data_opere(request):
    entry=Opera.objects.all()
    return render(request, 'mainopere.html', context={"export_record":entry, "elementi":entry.count()})

@login_required
def export_data_immagini(request):
    entry = Immagini.objects.all()
    return render(request, 'mainimmagini.html', context={"export_record":entry, "elementi":entry.count()})

@login_required
def opera_full(request):
    idval=request.GET['id']
    entry = Opera.objects.all().filter(id=idval)
    return render(request, 'opera_completa.html', context={"id":id,"entry":entry[0]})

