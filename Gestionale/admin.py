from django.contrib import admin
from django.contrib.admin import AdminSite
from django_extensions.admin import ForeignKeyAutocompleteAdmin
from import_export.admin import ImportExportModelAdmin
from simple_history.models import HistoricalRecords
from search_admin_autocomplete.admin import SearchAutoCompleteAdmin

from Gestionale.modelli_dati.Localiz import *
from Gestionale.modelli_dati.Restauro import *
from Gestionale.modelli_dati.DatiAnalitici import *
from Gestionale.modelli_dati.Giuridica import *

from jet.admin import CompactInline
from .models import *
from .viste import views as mainview

admin.site.site_header ="Binneale Incisione - Admin"
admin.site.site_title = "Binneale Incisione Portal"
admin.site.index_title = "Benvenuti sul portale della Binneale di Incisione"
admin.autodiscover()

class MyAdminSite(AdminSite):
    def get_urls(self):
        from django.conf.urls import url
        urls = super(MyAdminSite, self).get_urls()
        # Note that custom urls get pushed to the list (not appended)
        # This doesn't work with urls += ...
        urls = [
                url(r'^export/$', mainview.export_data, name='export')
        ] + urls
        return urls

admin_site = MyAdminSite()


class ImmaginiAdmin(ImportExportModelAdmin):


    def image_prew(self, obj):
        return mark_safe('<img src="/media/{0}" style="max-width:150px;height:auto">'.format(obj.preview))

    readonly_fields = ["image_prew","metainfo" ]
    list_display = ('id', "image_prew", 'titolo', "id_inventario", "image_meta_",)
    # search_fields = ['titolo',]
    list_filter=('titolo',)
    list_per_page = 25
    autocomplete_fields = ['titolo']

    fieldsets = [
        (None, {'fields': ['titolo']}),
        ('Immagini', {'fields': ['imagefile','imagefile1']}),
        ('Anteprima', {'fields': ['preview', 'preview1']}),
    ]

class AutoreAdmin(ImportExportModelAdmin):


    def image_prew(self, obj):
        return mark_safe('<img src="/media/{0}" style="max-width:100px;height:auto">'.format(obj.imagefile)
                     )
    readonly_fields = ["image_prew", ]
    list_display = ('id', 'titolo', 'nome', 'cognome', 'nascita', 'morte', 'stato', 'citta', 'indirizzo', 'telefono')
    search_fields = ('nome','cognome','indirizzo','citta','stato','telefono','mail')
    radio_fields = {"lingua": admin.HORIZONTAL,"genere": admin.HORIZONTAL}
    list_per_page = 25

class AutoreInline(CompactInline):
    model = Autore
    extra = 1
    show_change_link = True

class OperaAdmin(ImportExportModelAdmin, ForeignKeyAutocompleteAdmin):
    history = HistoricalRecords()

    def image_prew(self, obj):
        if obj.immagini:
            payload="{0}".format(obj.immagini.id)
        else:
            payload=""

        if obj.immagini:
            payload += mark_safe('<a href="/media/{0}" target="_blank"><img src="/media/{0}" style="max-width:150px;height:auto"></a>'.format(obj.immagini.preview))
        else:
            payload += mark_safe(
                '<a href="/media/{0}" target="_blank"><img src="/media/{0}" style="max-width:100px;height:auto"></a>'.format(
                    'logo_no_image.png'))
        return mark_safe(payload)

    related_search_fields = {'autore': ['cognome'], 'immagini':['id_inventario']}

    readonly_fields = ["image_prew", ]
    list_display = ['id', 'titolo_opera', 'autore', 'get_autore_nome', 'get_autore_cognome', 'riconoscimenti',
                    'posizione archivio', 'edizione', 'image_prew', 'abstract_', 'tag', ]
    search_fields = ('posizione_archivio', 'tag', 'titolo_opera')
    #filter=('titolo_opera','autore','get_autore_nome','get_autore_cognome','edizione','posizione_archivio','tag')
    list_filter = ('edizione', 'tags_s',)
    autocomplete_fields = ['autore', 'tags_s']
    list_per_page = 500

    ##Campi per l'esportazione dei dati
    #fields = ('id','titolo_opera','get_autore_nome','get_autore_cognome','riconoscimenti','pos_arch','edizione',   'image_prew', 'abstract_','tag')

    # Estrazioni chiavi esterne
    def get_autore_nome(self, obj):
        return obj.autore.nome
    get_autore_nome.admin_order_field  = 'Nome autore'  #Allows column order sorting
    get_autore_nome.short_description = 'Nome Autore'  #Renames column head

    def get_autore_cognome(self, obj):
        return obj.autore.cognome
    get_autore_cognome.admin_order_field  = 'Cognome autore'  #Allows column order sorting
    get_autore_cognome.short_description = 'Cognome Autore'  #Renames column head

class TagsAdmin(admin.ModelAdmin):
    list_display = ["nome", ]
    search_fields = ["nome"]

# Register your models here.
admin.site.register(Autore,AutoreAdmin)
admin.site.register(Opera,OperaAdmin)
admin.site.register(Immagini,ImmaginiAdmin)
admin.site.register(Tags, TagsAdmin)

# Voci schedatura
admin.site.register(Localizzazione)
admin.site.register(LocalizzazioneSpecifica)
admin.site.register(Restauro)
admin.site.register(DatiAnalitici)
admin.site.register(Iscrizioni)
admin.site.register(Giuridica)
