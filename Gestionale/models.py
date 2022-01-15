# coding=utf-8
"""
Gestionale d'arte
Il programma permette la gestione delle anagrafiche e delle opere d'arte. Il sistema e' stato creato per la gestione delle
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
from django.utils.encoding import smart_str
import urllib

MASK="000"
THUMB_SIZE=(600, 600)

# === Modelli dell'app Gestionale ===
""" Struttura per gestire le informazioni di angrafica necessarie per la
     gestione della corrispondenza e dell'archivio.
     """


def write_roman(num):
    """
    Funzione per la generazione dei numeni romani
    :param num:
    :return:
    """

    roman = OrderedDict()
    roman[1000] = "M"
    roman[900] = "CM"
    roman[500] = "D"
    roman[400] = "CD"
    roman[100] = "C"
    roman[90] = "XC"
    roman[50] = "L"
    roman[40] = "XL"
    roman[10] = "X"
    roman[9] = "IX"
    roman[5] = "V"
    roman[4] = "IV"
    roman[1] = "I"

    def roman_num(num):
        for r in roman.keys():
            x, y = divmod(num, r)
            yield roman[r] * x
            num -= (r * x)
            if num > 0:
                roman_num(num)
            else:
                break

    return "".join([a for a in roman_num(num)])



class Autore(models.Model):
    """
    Autore è il modello che gestisce i dati degli autori ed è collegato con chiavi esterne al
    :model:`Gestionale.Opera` e :model:`Gestionale.Immagini`

    **Variabili**
    TITLES : titoli.
    GENERE : genere.
    LINGUA  :  lingue parlate presenti nella scelta.
    """

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
    titolo=models.CharField(max_length=20,choices=TITLES,blank=True) #Il titolo può essere vuoto
    cognome = models.CharField(max_length=60, default='', help_text='Family name')
    nome=models.CharField(max_length=60,default='',help_text='Name')
    nascita = models.DateField(default='01/01/1900', blank=True, null=True, help_text='01/01/1988')

    #Dati di nascita della persona
    luogo_nascita=models.CharField(max_length=100,blank=False,default='')
    stato_nascita = models.CharField(max_length=100, blank=False,default='')
    genere=models.CharField(max_length=10,choices=GENERE,default='')

    #Dati residenza autore
    indirizzo = models.CharField(max_length=100,default='')
    citta = models.CharField(max_length=100,default='')
    provincia = models.CharField(max_length=60, default='')
    stato = models.CharField(max_length=60,default='')
    zip_code=models.CharField(max_length=60,default='')

    telefono = PhoneNumberField(default='', help_text='+393477093239 o 003321128832',blank=True, null=True)
    mobile = PhoneNumberField(default='', help_text='+393477093239 o 003321128832', blank=True, null= True)
    mail = models.EmailField(max_length=100,default='',blank=True, null= True, unique=False)
    website = models.CharField(default='',max_length=100, help_text='sitoweb www', blank=True, null=True)

    lingua = models.CharField(default='IT',choices=LINGUA, blank=False, null=False, max_length=60)
    imagefile = models.ImageField(db_column="imagefile", upload_to='pic_folder/autori', blank=True,help_text='immagine autore se presente')

    #history = HistoricalRecords()

    #Strutture accessorie
    #nome del record collegato alla vista del modello

    class Meta:
        """
        Indicazione del nome plurale per l'interfaccia di amministrazione
        """
        verbose_name_plural = "Autori"


    # === url ===
    def url(self):
        """
        Generazione del corretto link per la pubblicazione dei contenuti
        :return:
        """
        # returns a URL for either internal stored or external image url
        # if self.externalURL:
        #     return self.externalURL

        if not self.imagefile:
            return ''
        else:
            # is this the best way to do this??
            return os.path.join('/', settings.MEDIA_URL, os.path.basename(str(self.imagefile)))

    # === unicode ===
    def __unicode__(self):
        """
        Url dato in formato unicode
        :return:
        """
        return self.url()

    # === str ===
    def __str__(self):
        """
        Stringa base che appare nell'elenco dell voci ddei record della sezione admin
        :return:
        """
        return str(self.cognome+" "+self.nome)

    def image_(self):
        """
        Html per integrazione immagini anteprima (preview)
        :return:
        """

        return u'<a href="/media/{0}" target="_blank"><img src="/media/{0}" style="max-width:150px;height:auto"></a>'.format(
            self.imagefile)

    image_.allow_tags = True

    def save_low(self, force_insert=False, force_update=False):
        """
        Codifica dei campi nome e congnome ccon prima lettera maiuscola codificati in utf8
        :param force_insert:
        :param force_update:
        :return:
        """
        self.cognome=self.cognome.capitalize().encode('utf-8')
        self.nome = self.nome.capitalize().encode('utf-8')
        super(Autore, self).save(force_insert, force_update)



class Immagini(models.Model):
    """
         Modello per la memorizzaizione dei dati, immagini delle opere d'arte.


         """
    #Record base
    datestamp = models.DateTimeField(auto_now_add=True)

    #Modello dati
    titolo = models.ForeignKey('Opera', on_delete=models.DO_NOTHING, default='',blank=True,related_name="img_titolo_opera",null=True)
    commento=models.TextField(default="",help_text="breve commento all'opera o note", blank=True)
    imagefile = models.ImageField(db_column="imagefile",upload_to='pic_folder/opere', blank=True, default="logo_no_image.png")
    imagefile1 = models.ImageField(db_column="imagefile1", upload_to='pic_folder/opere/im1', blank=True)
    imagefile2 = models.ImageField(db_column="imagefile2", upload_to='pic_folder/opere/im2', blank=True)
    preview = models.ImageField(db_column="preview", upload_to='pic_folder/opere/preview', blank=True)
    preview1 = models.ImageField(db_column="preview1", upload_to='pic_folder/opere/preview1', blank=True)
    metainfo=models.TextField(default='',blank=True)

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
            # title = self.titolo.posizione_archivio + " - " + self.titolo.autore.cognome + " - " + self.titolo.titolo_opera + " / " + self.titolo.anno_realizzazione.__str__()

            title=self.titolo.posizione_archivio + " - " + self.titolo.autore.cognome + " - / " + str(self.titolo.anno_realizzazione)
            return str(title)
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
        PIL_TYPE = 'jpeg'
        FILE_EXTENSION = 'jpg'
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
        image = Image.open(settings.BASE_DIR+urllib.parse.unquote(self.imagefile.url))
        if image.mode in ("RGBA", "P"):
            image = image.convert("RGB")

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
        imagepath='%s_thumbnail.%s' % (os.path.splitext(suf.name)[0], FILE_EXTENSION)
        self.preview.save(imagepath,suf,save=True)


    image_meta_.allow_tag=True


    class Meta:
        verbose_name_plural = "Immagini"

    def save(self):

        self.metainfo=self.image_meta_()
        #creazione immagine anteprima
        #self.make_thumbnail()
        super(Immagini, self).save()


class Opera(models.Model):

    #Modello dati
    #riferimento esterno
    #id=models.IntegerField(primary_key=True,auto_created=True,blank=None,editable=False)
    autore=models.ForeignKey('Autore', on_delete=models.DO_NOTHING,related_name='autore',blank=True,)
    titolo_opera = models.CharField(max_length=400, default='')
    descrizione = models.TextField( default='',blank=True, null= True)

    nazione = models.CharField(max_length=60, default='')
    riconoscimenti = models.CharField(max_length=60, default='',blank=True, null= True)

    #Dati opera
    dimensione_lastra=models.CharField(max_length=25, default='')
    dimensione_lastra_y = models.IntegerField(default=0, help_text="dimensione in mm")
    dimensione_lastra_x = models.IntegerField(default=0, help_text="dimensione in mm")
    dimensione_foglio_y = models.IntegerField(default=0, help_text="dimensione in mm")
    dimensione_foglio_x = models.IntegerField(default=0, help_text="dimensione in mm")

    #numero_lastre = models.IntegerField(default=0, help_text="")
    tecnica = models.CharField(max_length=500, default='')

    anno_realizzazione = models.IntegerField(default=datetime.datetime.now().year)

    # Permette la scelta solo negli ultimi due anni
    anni=[a for a in range(1993,datetime.date.today().year+2)[::2]]
    EDIZIONI = [(str(write_roman(int((a-1993)/2)+1)+' Biennale - '+str(a)),str(write_roman(int((a-1993)/2)+1)+'- Biennale -'+str(a))) for a in anni]
    EDIZIONI= EDIZIONI[::-1] #reverse array
    EDIZIONI.append(("DA CANCELLARE",'DA CANCELLARE'))
    EDIZIONI.append(("NON IN CONCORSO",'NON IN CONCORSO'))

    #YEARS=[(r,r) for r in range(datetime.datetime.now().year-1,datetime.datetime.now().year+1)]
    #anno_presentazione = models.IntegerField( choices=YEARS, default=datetime.datetime.now().year)
    edizione = models.TextField(max_length=60, choices=EDIZIONI, default=EDIZIONI[0][0], blank=True)


    #commento_opera = models.TextField(default="", help_text="breve commento all'opera o note",blank=True)
    note = models.TextField(max_length=500, default='',blank=True)
    posizione_archivio = models.CharField(max_length=60, default='')


    #Non è obbligatorio avere l'immagine da collegare
    immagini=models.ForeignKey(Immagini,on_delete=models.CASCADE,default='',blank=True, null=True)
    tag=models.TextField(max_length=200,default='', help_text="inserire i tag separati da una virgola")


    #history = HistoricalRecords()


    def immagini_(self):
        print(self.immagini)
        if self.immagini == None :
            return u'<a href="/media/logo_no_image.png" target="_blank"><img src="/media/logo_no_image.png" style="max-width:150px;height:auto"></a>'
        else:
            return u'<a href="/media/{0}" target="_blank"><img src="/media/{0}" style="max-width:150px;height:auto"></a>'.format(self.immagini)

    immagini_.allow_tags = True

    #Strutture accessorie
    #nome del record collegato alla vista del modello
    def __str__(self):
        # return self.posizione_archivio+" - "+self.autore.cognome+" - "+self.titolo_opera+" / "+self.anno_realizzazione.__str__()
        title = self.posizione_archivio + " - " + self.autore.cognome + " - / " + self.anno_realizzazione.__str__()
        return str(title.encode('utf-8'))

    def indicazione_(self):
        return self.titolo_opera + " / " + self.anno_realizzazione.__str__()
    indicazione_.allow_tag=True

    def abstract_(self):
        abst="tecnica:"+self.tecnica + " | anno:" + self.anno_realizzazione.__str__()+' | misure lastra:'

        if self.dimensione_lastra:
            abst+=self.dimensione_lastra
        else:
            abst+=self.dimensione_lastra_x.__str__()+"X"+self.dimensione_lastra_y.__str__()+ \
               " / "+self.dimensione_foglio_x.__str__()+"X"+self.dimensione_foglio_y.__str__()

        return abst

    abstract_.allow_tag = True

    def pos_arch(self):
        return str(MASK[0:len(MASK)-len(self.posizione_archivio)]+self.posizione_archivio)

    def save_low(self, force_insert=False, force_update=False):
        self.titolo_opera = self.titolo_opera.capitalize().encode('utf-8')
        self.nazione=self.nazione.capitalize().encode('utf-8')
        self.tag=self.tag.lower().encode('utf-8')
        self.autore.cognome=self.autore.cognome.capitalize().encode('utf-8')
        self.autore.nome = self.autore.nome.capitalize().encode('utf-8')


        super(Opera, self).save(force_insert, force_update)

    class Meta:
        verbose_name_plural = "Opere"






