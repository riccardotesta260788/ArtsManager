from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from Gestionale.models import *


#from .mongo_models import *


def home(request):
    return render(request, 'homepageNotLog.html', context={"message": "Home page"})


def login(request):
    return render(request, 'registration/login.html', context={})


def handler404(request, *args, **argv):
    return render(request, 'errors.html', status=404, context={"errore": '404',
                                                               "message":"Pagina non trovata"})

def handler500(request, *args, **argv):
    return render(request, 'errors.html', status=500, context={"errore": '500',
                                                              "message":"Errore del server"})

@login_required
def export_data_autori(request):
    entry = Autore.objects.all().order_by('cognome').distinct()
    return render(request, 'pages/mainautori.html', context={"export_record":entry, "elementi":entry.count()})

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
    return render(request, 'opera_completa.html', context={"id":id, "entry":entry[0]})



@login_required
def opere_list_full(request):
    entry = Opera.objects.all().order_by('posizione_archivio')
    return render(request, 'opere_lista_completa.html', context={"id":id, "entries":entry})

# Lista ultima edizione
@login_required
def opere_list_full_last(request):
    print(Opera.EDIZIONI[0][1])
    edizione = 'XVI- Biennale -2023'
    entry = Opera.objects.all().filter(edizione=edizione).order_by('posizione_archivio')
    return render(request, 'opere_lista_completa.html', context={"id":id, "entries":entry})


@login_required
def opere_list_full_autori(request):
    entry = Opera.objects.all().order_by("autore__cognome")
    return render(request, 'opere_lista_completa_autore.html', context={"id":id, "entries":entry})

@login_required
def autori_full(request):
    autori = Autore.objects.all().distinct().order_by('cognome')
    return render(request, 'mainautorilist.html', context={"id":id, "autori":autori})

@login_required
def backup(request):
    files=[]

    import os, fnmatch

    listOfFiles = os.listdir('../../../../backup')
    pattern = "*.dump"
    for entry in listOfFiles:
        if fnmatch.fnmatch(entry, pattern):
            print(entry)

    return render(request, 'listBackup.html', context={"files":files})

'''
--------- Utilities section   -----------
'''

@login_required
def utilities(request):

    return render(request, 'utilities.html', context={"message": "Home page"})

@login_required
def lower_case(request):
    #Richiama la funzione di salvataggio di ogni singolo modello specializzata
    # per i testi in minuscolo

    entries = Autore.objects.all()
    for entry in entries:
        entry.save_low()
        print(entry)

    entries = Opera.objects.all()
    for entry in entries:
        entry.save_low()
        print(entry)

    return render(request, 'utilities.html', context={"lower": entries.count()})


@login_required
def mongosave(request):
    from pymodm import connect

    # Establish a connection to the database and call the connection my-atlas-app
    connect(
        'mongodb+srv://riccardo:riki88@biennale2018-rhtxe.mongodb.net/Biennale?retryWrites=true',
        alias='biennale')

    opere=Opera.objects.all()

    '''
        for opera in opere:
            oper=MOpera()
            oper=opera
            oper.autore=opera.autore
            oper.save()
    
    
    '''


    return render(request, 'utilities.html', context={"dbtest": "ok"})

#Eportazione documentazione
@login_required
def adress_plaque(request):
    entries = Autore.objects.all().order_by('cognome')

    # for entry in entries:
    #     entry.save_low()
    # print(entry)
    # Richiesta asincrona


    return render(request, 'doc_export/export_plaque.html', context={"autori": entries})

#Eportazione documentazione
@login_required
def elenco_alfa(request):
    entries = Autore.objects.all().order_by('cognome')
    for entry in entries:
        entry.save_low()
        print(entry)

    return render(request, 'doc_export/elenco_alfa.html', context={"autori": entries})