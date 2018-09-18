import os
from django.db import models,migrations
from django.views import generic
from phonenumber_field.modelfields import PhoneNumberField
import datetime
from django.conf import settings
from django.utils.safestring import mark_safe
import PIL





class Autore(models.Model):
    TITLES = (
        ('Mr', 'Sig'),
        ('Mrs', 'Signora'),
        ('Dott', 'Dottore'),
        ('Dott.ssa', 'Dottoressa'),
        ('Prof', 'Professore'),
    )
    GENERE = (
        ('male', 'Maschio'),
        ('female', 'Femmina'),

    )
    LINGUA = (
        ('IT - Italiano', 'Italiano'),
        ('EN - Inglese', 'Inglese'),
        ('FR - Francese', 'Francese'),
        ('DE - Tedesco', 'Tedesco'),
        ('SP - Spagnolo', 'Spagnolo'),
        ('PT - Portoghese', 'Portoghese'),

    )

    #Modello dati
    titolo=models.CharField(max_length=20,choices=TITLES,blank=True) #Il titolo può essere vuoto

    nome=models.CharField(max_length=60,default='',help_text='Name')
    cognome=models.CharField(max_length=60, default='',help_text='Family name')
    nascita = models.DateField(default='01/01/1900', blank=False, null=False,help_text='01/01/1988')

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

    telefono = PhoneNumberField(default='', help_text='+393477093239 o 003321128832',blank=False, null=False)
    mail = models.EmailField(max_length=100,default='',blank=True, null= True, unique= True)

    lingua = models.CharField(default='IT',choices=LINGUA, blank=False, null=False, max_length=60)
    imagefile = models.ImageField(db_column='imagefile', upload_to='pic_folder/autori', blank=True,help_text='immagine autore se presente')

    #Strutture accessorie
    #nome del record collegato alla vista del modello
    def __str__(self):
        return self.cognome+" "+self.nome

    class Meta:
        verbose_name_plural = "Autori"


    # Strutture accessorie
    def url(self):
        # returns a URL for either internal stored or external image url
        if self.externalURL:
            return self.externalURL
        else:
            # is this the best way to do this??
            return os.path.join('/', settings.MEDIA_URL, os.path.basename(str(self.image)))

    def __unicode__(self):
        return self.image.url

    def __str__(self):
        return self.cognome+" "+self.nome

    def image_(self):
        return u'<a href="/media/{0}" target="_blank"><img src="/media/{0}" style="max-width:150px;height:auto"></a>'.format(
            self.imagefile)

    image_.allow_tags = True



class Immagini(models.Model):
    #Record base
    datestamp = models.DateTimeField(auto_now_add=True)

    #Modello dati
    autore = models.ForeignKey('Autore', on_delete=models.CASCADE, related_name='uploaded_documents',default='')
    titolo_opera = models.CharField(max_length=60, default='')
    commento=models.TextField(default="",help_text="breve commento all'opera o note", blank=True)
    imagefile = models.ImageField(db_column='imagefile',upload_to='pic_folder/opere', blank=True)
    metainfo=models.TextField(default='',blank=True)


    #Strutture accessorie
    def url(self):
        # returns a URL for either internal stored or external image url
        if self.externalURL:
            return self.externalURL
        else:
            # is this the best way to do this??
            return os.path.join('/', settings.MEDIA_URL, os.path.basename(str(self.imagefile)))

    def __unicode__(self):
        return self.imagefile.url

    def __str__(self):
        return self.titolo_opera

    def image_(self):
        return mark_safe('<a href="/media/{0}"><img src="/media/{0}" style="max-width:150px;height:auto"></a>'.format(self.imagefile))

    image_.allow_tags = True

    def image_meta_(self):

        image_meta=PIL.Image.open(self.imagefile)
        weight=self.imagefile.file.size
        weight=weight/1024
        dpi=""

        if image_meta:
            size=image_meta.size
            if hasattr(image_meta.info,'dpi'):
                dpi=image_meta.info['dpi']
            else:
                dpi="Non presente"


        return mark_safe('Dimensione immagine:{0}x{1} DPI:{2} {3} KB'.format(size[0],size[1],dpi,round(weight)))


    image_meta_.allow_tag=True

    class Meta:
        verbose_name_plural = "Immagini"

    def save(self):

        self.metainfo=self.image_meta_()
        super(Immagini, self).save()






class Opera(models.Model):

    #Modello dati
    #riferimento esterno
    id=models.IntegerField(primary_key=True,auto_created=True,blank=None,unique=True,editable=False)
    autore=models.ForeignKey('Autore', on_delete=models.CASCADE, default='',related_name='autore',blank=True,)
    titolo_opera = models.CharField(max_length=60, default='')
    descrizione = models.TextField( default='')

    nazione = models.CharField(max_length=60, default='')
    riconoscimenti = models.CharField(max_length=60, default='')

    #Dati opera
    dimensione_lastra_x = models.IntegerField(default=0, help_text="dimensione in mm")
    dimensione_lastra_y = models.IntegerField(default=0, help_text="dimensione in mm")
    dimensione_foglio_x = models.IntegerField(default=0, help_text="dimensione in mm")
    dimensione_foglio_y = models.IntegerField(default=0, help_text="dimensione in mm")
    numero_lastre = models.IntegerField(default=0, help_text="")
    tecnica = models.CharField(max_length=80, default='')

    # Permette la scelta solo negli ultimi due anni
    YEAR_CHOICES = [(r, r) for r in range(datetime.date.today().year -1, datetime.date.today().year+1)]
    anno_realizzazione = models.IntegerField(default=datetime.datetime.now().year)
    anno_presentazione = models.IntegerField(choices=YEAR_CHOICES, default=datetime.datetime.now().year)

    commento_opera = models.TextField(default="", help_text="breve commento all'opera o note",blank=True)
    note = models.TextField(max_length=60, default='',blank=True)
    posizione_archivio = models.CharField(max_length=60, default='')


    immagini=models.ForeignKey(Immagini,on_delete=models.CASCADE,default='')
    tag=models.TextField(max_length=200,default='', help_text="inserire i tag separati da una virgola")



    def immagini_(self):
        return u'<a href="/media/{0}" target="_blank"><img src="/media/{0}" style="max-width:150px;height:auto"></a>'.format(self.immagini.imagefile)

    immagini_.allow_tags = True

    #Strutture accessorie
    #nome del record collegato alla vista del modello
    def __str__(self):
        return self.titolo_opera+" / "+self.anno_realizzazione.__str__()

    def indicazione_(self):
        return self.titolo_opera + " / " + self.anno_realizzazione.__str__()
    indicazione_.allow_tag=True

    def abstract_(self):
        return "tecnica:"+self.tecnica + " / anno:" + self.anno_realizzazione.__str__()+'/ misure lastra:'+\
               self.dimensione_lastra_x.__str__()+"X"+self.dimensione_lastra_y.__str__()+\
               " / "+self.dimensione_foglio_x.__str__()+"X"+self.dimensione_foglio_y.__str__()

    abstract_.allow_tag = True


    class Meta:
        verbose_name_plural = "Opere"
