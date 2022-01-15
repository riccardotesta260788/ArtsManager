from django.shortcuts import render
from django.http import HttpResponse
import datetime
from django.template.loader import get_template
from Gestionale.models import *
from django.conf import settings
from django.contrib.auth.decorators import login_required

MEDIA=settings.BASE_DIR

def meta_size(path):
    path=str(MEDIA+path.url)
    file_size = os.path.getsize(path)
    # imagefile = PIL.Image.open(path)
    # weight = imagefile.file.size
    # weight = weight / 1024
    print(path,file_size)
    return file_size,

def isfile(path):
    pathr=MEDIA+path
    return os.path.isfile(pathr)

def right_path(path):
    p='pic_folder/opere/preview/'
    pathsplit=path.split('/')
    name=pathsplit[-1].split('.')
    rname=name[0]+'_thumbnail.'+name[1]
    return p+rname

def make_thumbnail(path):

    if not path:
        return

    from PIL import Image
    from io import StringIO
    from django.core.files.uploadedfile import SimpleUploadedFile
    import os

    # Set our max thumbnail size in a tuple (max width, max height)
    THUMBNAIL_SIZE = (400, 400)
    PIL_TYPE = 'tiff'
    FILE_EXTENSION = 'tiff'


    # Open original photo which we want to thumbnail using PIL's Image
    image = Image.open(path)

    # We use our PIL Image object to create the thumbnail, which already
    # has a thumbnail() convenience method that contrains proportions.
    # Additionally, we use Image.ANTIALIAS to make the image look better.
    # Without antialiasing the image pattern artifacts may result.
    image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)

    # Save the thumbnail
    temp_handle = BytesIO()
    image.save(temp_handle, PIL_TYPE)
    temp_handle.seek(0)

    # Save image to a SimpleUploadedFile which can be saved into
    # ImageField
    savepath=os.path.split(path)[-1]
    suf = SimpleUploadedFile(os.path.split(path)[-1],
                             temp_handle.read())
    return savepath

@login_required
def compress_images_previews(request):
    entry=Opera.objects.all()
    html=""

    for obj in entry:
       if obj.edizione=='XV- Biennale -2021':
           obj.edizione='XV Biennale - 2021'
           print(obj.titolo_opera)
           obj.save()

    return HttpResponse(html)

def correct_images_previews(request):
    entry=Immagini.objects.all()
    html=""

    for obj in entry:
        print(obj)
        # if  obj.id>205 and not str(obj.preview.url).endswith('.jpg'):
        if  obj.id<205 :
            # if(obj.imagefile.url==obj.preview.url and obj.preview.url):
            # stessa immagine
            print(obj)
            # obj.preview=right_path(obj.imagefile.url)
            # obj.save()
            obj.make_thumbnail()
            html+='Correct - {} to {}<hr>\n'.format(str(obj.imagefile.url),str(obj.preview.url))


    return HttpResponse(html)

'''
Utiliti per il debug del codice'''
class dbs:
    data="----\n<br>DEBUG\n <br>----"
    def add(self,datap):
        self.data=self.data+str(datap)+'\n<br>'
    def get(self):
        return self.data

'''
Eliminazione di caratteri non conformi dai campi dei modelli
'''
from django.apps import apps #caricamento dinamico moduli
def purgeCaracters(request, model,field):
    #Il nome interno dell'app è Gestionale
    model = apps.get_model('Gestionale', model)

    dbug=dbs()

    for entry in model.objects.all():
        dbug.add('pre: '+entry.field)
        dbug.add('after: '+entry.field)

    return HttpResponse(dbug.get())

