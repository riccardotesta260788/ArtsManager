# Librerire esterne
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.http import HttpResponse
from docx.shared import Mm
from docxtpl import DocxTemplate, InlineImage

# Sistema
from Gestionale.models import *


@login_required
def document(request):
    response = HttpResponse(content_type='application/msword')
    response['Content-Disposition'] = 'attachment; filename="elenco_generale.docx"'
    doc = DocxTemplate(str(settings.BASE_DIR) + '/templates/word_doc/base.docx')

    # The image must be already saved on the disk
    # reading images from url is not supported

    print(Opera.EDIZIONI[0][1])
    # entry = Opera.objects.all().filter(edizione=Opera.EDIZIONI[1][0]).order_by('posizione_archivio')
    entry = Opera.objects.all().filter(edizione='XVI- Biennale -2023').order_by('posizione_archivio')
    imagen = InlineImage(doc, entry[0].immagini.preview, width=Mm(20))  # width is in millimetres

    context = {'i': str.join(',', [f.name for f in Opera._meta.get_fields()])}

    context = model_to_dict(entry[0])

    doc.render(context)
    doc.save(response)

    return response
