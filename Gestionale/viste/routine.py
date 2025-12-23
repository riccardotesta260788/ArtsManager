from django.http import HttpResponse
from django.shortcuts import render
from Gestionale.models import *
from django.contrib.auth.decorators import login_required


def extract_tags(request):
    el = Opera.objects.all()
    iter = 0

    for obj in el:
        # Estrazione tag delle singole voci
        tags = obj.tag.split(',')

        for tag in tags:
            # controllo che il tag non sia già presente

            tag = tag.lower()
            tag = tag.strip()

            if not Tags.objects.filter(nome=tag):
                tag_ob = Tags(nome=tag)
                print('%d - Aggiunto: %s\n' % (iter, tag))
                iter += 1
                tag_ob.save()

    return HttpResponse("Terminato")
