"""
Gestionale d'arte
Il programma permette la gestione delle anagrafiche e delle opere d'arte. Il sistema è stato creato per la gestione delle
inormazioni e dei dati per le mostre d'arte o per eventi.

1. **Autore** - Anagrafica Autore
2. **Opera** - Anagrafica Opere
3. **Immagini** - Gestione immagini Opere
"""

import os
from io import StringIO,BytesIO
from django.db import models,migrations
from django.views import generic
from phonenumber_field.modelfields import PhoneNumberField
import datetime
from django.conf import settings
from django.utils.safestring import mark_safe
import PIL
from django import forms
from collections import OrderedDict
from PIL import Image as Img
from django.conf import settings
from django.core.files import temp as tempfile
from django.core.files.base import File
from pymodm import MongoModel
from pymodm import MongoModel, fields
from pymongo.write_concern import WriteConcern



class MAutore(MongoModel):

    #Titolo
    TITLES = (
        ('Mr', 'Sig'),
        ('Mrs', 'Signora'),
        ('Dott', 'Dottore'),
        ('Dott.ssa', 'Dottoressa'),
        ('Prof', 'Professore'),
        ('Prof.ssa', 'Professoressa'),
    )
    #Genere
    GENERE = (
        ('male', 'Maschio'),
        ('female', 'Femmina'),

    )
    #Lingua
    LINGUA = (
        ('IT - Italiano', 'Italiano'),
        ('EN - Inglese', 'Inglese'),
        ('FR - Francese', 'Francese'),
        ('DE - Tedesco', 'Tedesco'),
        ('SP - Spagnolo', 'Spagnolo'),
        ('PT - Portoghese', 'Portoghese'),

    )

    # === Campi ===
    titolo=fields.CharField(max_length=20,choices=TITLES,blank=True) #Il titolo può essere vuoto
    cognome = fields.CharField(max_length=60, default='', help_text='Family name')
    nome=fields.CharField(max_length=60,default='',help_text='Name')
    nascita = fields.DateField(default='01/01/1900', blank=True, null=True, help_text='01/01/1988')

    #Dati di nascita della persona
    luogo_nascita=fields.CharField(max_length=100,blank=False,default='')
    stato_nascita = fields.CharField(max_length=100, blank=False,default='')
    genere=fields.CharField(max_length=10,choices=GENERE,default='')

    #Dati residenza autore
    indirizzo = fields.CharField(max_length=100,default='')
    citta = fields.CharField(max_length=100,default='')
    provincia = fields.CharField(max_length=60, default='')
    stato = fields.CharField(max_length=60,default='')
    zip_code=fields.CharField(max_length=60,default='')

    telefono = PhoneNumberField(default='', help_text='+393477093239 o 003321128832',blank=True, null=True)
    mobile = PhoneNumberField(default='', help_text='+393477093239 o 003321128832', blank=True, null= True)
    mail = fields.EmailField(max_length=100,default='',blank=True, null= True, unique= True)
    website = fields.CharField(default='',max_length=100, help_text='sitoweb www', blank=True, null=True)

    lingua = fields.CharField(default='IT',choices=LINGUA, blank=False, null=False, max_length=60)
    imagefile = fields.ImageField(db_column='imagefile', upload_to='pic_folder/autori', blank=True,help_text='immagine autore se presente')

    #history = HistoricalRecords()

    #Strutture accessorie
    #nome del record collegato alla vista del modello
    def __str__(self):
        return self.cognome+" "+self.nome

    class Meta:
        verbose_name_plural = "Autori"


    # === url ===
    def url(self):
        # returns a URL for either internal stored or external image url
        if self.externalURL:
            return self.externalURL
        else:
            # is this the best way to do this??
            return os.path.join('/', settings.MEDIA_URL, os.path.basename(str(self.image)))

    # === unicode ===
    def __unicode__(self):
        return self.image.url

    # === str ===
    def __str__(self):
        return self.cognome+" "+self.nome

    def image_(self):
        return u'<a href="/media/{0}" target="_blank"><img src="/media/{0}" style="max-width:150px;height:auto"></a>'.format(
            self.imagefile)

    image_.allow_tags = True

    def save_low(self, force_insert=False, force_update=False):
        self.cognome=self.cognome.capitalize()
        self.nome = self.nome.capitalize()
        super(MAutore, self).save(force_insert, force_update)



class MImmagini(MongoModel):
    """
         Modello per la memorizzaizione dei dati, immagini delle opere d'arte.
         """
    #Record base
    datestamp = fields.DateTimeField(auto_now_add=True)

    #Modello dati
    titolo = fields.ForeignKey('Opera', on_delete=fields.CASCADE, default='',blank=True,related_name="img_titolo_opera",null=True)
    commento=fields.TextField(default="",help_text="breve commento all'opera o note", blank=True)
    imagefile = fields.ImageField(db_column='imagefile',upload_to='pic_folder/opere', blank=True, default="logo_no_image.png")
    imagefile1 = fields.ImageField(db_column='imagefile1', upload_to='pic_folder/opere/im1', blank=True)
    imagefile2 = fields.ImageField(db_column='imagefile2', upload_to='pic_folder/opere/im2', blank=True)
    preview = fields.ImageField(db_column='preview', upload_to='pic_folder/opere/preview', blank=True)
    preview1 = fields.ImageField(db_column='preview1', upload_to='pic_folder/opere/preview1', blank=True)
    metainfo=fields.TextField(default='',blank=True)

    #history = HistoricalRecords()
    #Strutture accessorie



    def url(self):
        # returns a URL for either internal stored or external image url
        if self.externalURL:
            return self.externalURL
        else:

            return os.path.join('/', settings.MEDIA_URL, os.path.basename(str(self.imagefile)))

    def __unicode__(self):
        return self.imagefile.url

    def __str__(self):

        if(self.titolo):
            return self.titolo.posizione_archivio + " - " + self.titolo.autore.cognome + " - " + self.titolo.titolo_opera + " / " + self.titolo.anno_realizzazione.__str__()
            # self.titolo.titolo_opera
        else:
            return "RIFERIMENTO VUOTO"

    def image_(self):
        return mark_safe('<a href="/media/{0}"><img src="/media/{0}" style="max-width:150px;height:auto"></a>'.format(self.preview))

    image_.allow_tags = True

    def image_meta_(self):

        image_meta = PIL.Image.open(self.imagefile)
        weight = self.imagefile.file.size
        weight = weight / 1024
        dpi = ""

        if image_meta:
            size = image_meta.size
            if hasattr(image_meta.info, 'dpi'):
                dpi = image_meta.info['dpi']
            else:
                dpi = "Non presente"

        return mark_safe('Dimensione immagine:{0}x{1} DPI:{2} {3} KB'.format(size[0], size[1], dpi, round(weight)))

    def make_thumbnail(self):
        # original code for this method came from
        # http://snipt.net/danfreak/generate-thumbnails-in-django-with-pil/

        # If there is no image associated with this.
        # do not create thumbnail
        if not self.imagefile:
            return

        from PIL import Image
        from io import StringIO
        from django.core.files.uploadedfile import SimpleUploadedFile
        import os

        # Set our max thumbnail size in a tuple (max width, max height)
        THUMBNAIL_SIZE = (400, 400)
        PIL_TYPE = 'tiff'
        FILE_EXTENSION = 'tiff'
        '''
        DJANGO_TYPE = self.imagefile.file.content_type

        if DJANGO_TYPE == 'image/jpeg':
            PIL_TYPE = 'jpeg'
            FILE_EXTENSION = 'jpg'
        elif DJANGO_TYPE == 'image/png':
            PIL_TYPE = 'png'
            FILE_EXTENSION = 'png'
        elif DJANGO_TYPE == 'image/tiff':

'''

        # Open original photo which we want to thumbnail using PIL's Image
        image = Image.open("media/"+self.imagefile.name)

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
        suf = SimpleUploadedFile(os.path.split(self.imagefile.name)[-1],
                temp_handle.read())


        # Save SimpleUploadedFile into image field
        self.preview.save(
            '%s_thumbnail.%s' % (os.path.splitext(suf.name)[0], FILE_EXTENSION),
            suf,
            save=False
        )


    image_meta_.allow_tag=True


    class Meta:
        verbose_name_plural = "Immagini"

    def save(self):

        self.metainfo=self.image_meta_()
        #creazione immagine anteprima
        #self.make_thumbnail()
        super(MImmagini, self).save()






class MOpera(MongoModel):

    #Modello dati
    #riferimento esterno
    #id=fields.IntegerField(primary_key=True,auto_created=True,blank=None,editable=False)
    autore=fields.ForeignKey('Autore', on_delete=fields.CASCADE, default='',related_name='autore',blank=True,)
    titolo_opera = fields.CharField(max_length=120, default='')
    descrizione = fields.TextField( default='',blank=True, null= True)

    nazione = fields.CharField(max_length=60, default='')
    riconoscimenti = fields.CharField(max_length=60, default='',blank=True, null= True)

    #Dati opera
    dimensione_lastra_y = fields.IntegerField(default=0, help_text="dimensione in mm")
    dimensione_lastra_x = fields.IntegerField(default=0, help_text="dimensione in mm")
    dimensione_foglio_y = fields.IntegerField(default=0, help_text="dimensione in mm")
    dimensione_foglio_x = fields.IntegerField(default=0, help_text="dimensione in mm")

    #numero_lastre = fields.IntegerField(default=0, help_text="")
    tecnica = fields.CharField(max_length=80, default='')

    anno_realizzazione = fields.IntegerField(default=datetime.datetime.now().year)

    # Permette la scelta solo negli ultimi due anni
    anni=[a for a in range(1993,datetime.date.today().year+2)[::2]]
    EDIZIONI = [(str(write_roman(int((a-1993)/2)+1)+'- Biennale -'+str(a)),str(write_roman(int((a-1993)/2)+1)+'- Biennale -'+str(a))) for a in anni]
    EDIZIONI= EDIZIONI[::-1] #reverse array

    #YEARS=[(r,r) for r in range(datetime.datetime.now().year-1,datetime.datetime.now().year+1)]
    #anno_presentazione = fields.IntegerField( choices=YEARS, default=datetime.datetime.now().year)
    edizione = fields.TextField(max_length=60, choices=EDIZIONI, default=EDIZIONI[0])


    #commento_opera = fields.TextField(default="", help_text="breve commento all'opera o note",blank=True)
    note = fields.TextField(max_length=60, default='',blank=True)
    posizione_archivio = fields.CharField(max_length=60, default='')


    #Non è obbligatorio avere l'immagine da collegare
    immagini=fields.ForeignKey(Immagini,on_delete=fields.CASCADE,default='',blank=True, null=True)
    tag=fields.TextField(max_length=200,default='', help_text="inserire i tag separati da una virgola")

    #history = HistoricalRecords()


    def immagini_(self):
        #if self.immagini == None :
            return u'<a href="/media/logo_no_image.png" target="_blank"><img src="/media/logo_no_image.png" style="max-width:150px;height:auto"></a>'
        #else:
            #return u'<a href="/media/{0}" target="_blank"><img src="/media/{0}" style="max-width:150px;height:auto"></a>'.format(self.immagini)

    immagini_.allow_tags = True

    #Strutture accessorie
    #nome del record collegato alla vista del modello
    def __str__(self):
        return self.posizione_archivio+" - "+self.autore.cognome+" - "+self.titolo_opera+" / "+self.anno_realizzazione.__str__()

    def indicazione_(self):
        return self.titolo_opera + " / " + self.anno_realizzazione.__str__()
    indicazione_.allow_tag=True

    def abstract_(self):
        return "tecnica:"+self.tecnica + " / anno:" + self.anno_realizzazione.__str__()+'/ misure lastra:'+ \
               self.dimensione_lastra_x.__str__()+"X"+self.dimensione_lastra_y.__str__()+ \
               " / "+self.dimensione_foglio_x.__str__()+"X"+self.dimensione_foglio_y.__str__()

    abstract_.allow_tag = True

    def pos_arch(self):
        return str(MASK[0:len(MASK)-len(self.posizione_archivio)]+self.posizione_archivio)

    def save_low(self, force_insert=False, force_update=False):
        self.titolo_opera = self.titolo_opera.capitalize()
        self.nazione=self.nazione.capitalize()
        self.tag=self.tag.lower()
        self.autore.cognome=self.autore.cognome.capitalize()
        self.autore.nome = self.autore.nome.capitalize()


        super(MOpera, self).save(force_insert, force_update)

    class Meta:
        verbose_name_plural = "Opere"






