from django.shortcuts import render
from django.http import HttpResponse
import datetime
from django.template.loader import get_template
from Gestionale.models import *
from django.conf import settings
from django.contrib.auth.decorators import login_required

#estrazione dei dati in formato json o seriale per parsing
from django.core import serializers
from django.forms.models import model_to_dict
import json



MEDIA=settings.BASE_DIR
WORD_TEMPLATE=os.path.join(settings.BASE_DIR, 'templates/word_doc/')

def main(request):
    doc = DocxTemplate(WORD_TEMPLATE+"base.docx")
    # ... your other code ...

    doc_io = io.BytesIO() # create a file-like object
    doc.save(doc_io) # save data to file-like object
    doc_io.seek(0) # go to the beginning of the file-like object

    response = HttpResponse(doc_io.read())

    # Content-Disposition header makes a file downloadable
    response["Content-Disposition"] = "attachment; filename=generated_doc.docx"

    # Set the appropriate Content-Type for docx file
    response["Content-Type"] = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    return HttpResponse(html)

def docx(request):
    response_data = {}
    entries=Opera.objects.all()
    SomeModel_json = serializers.serialize("json", entries)
    data = json.dumps(SomeModel_json)
    return HttpResponse(data)