from django.contrib import admin

from .models import *
from django.contrib.admin import AdminSite
from .viste import views as mainview
from jet.admin import CompactInline
from import_export.admin import ImportExportModelAdmin


admin.site.site_header ="Binneale Incisione - Admin"
admin.site.site_title = "Binneale Incisione Portal"
admin.site.index_title = "Benvenuti sul portale della Binneale di Incisione"

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
    list_display = ('titolo',"image_meta_","image_prew")
    search_fields = ('titolo',)
    list_filter=('titolo',)
    list_per_page = 25

    fieldsets = [
        (None, {'fields': ['titolo']}),
        ('Immagini', {'fields': ['imagefile','imagefile1']}),
        ('Anteprima', {'fields': ['preview', 'preview1']}),
    ]

class AutoreAdmin(ImportExportModelAdmin):


    def image_prew(self, obj):
        return mark_safe('<img src="/media/{0}" style="max-width:150px;height:auto">'.format(obj.imagefile)
                     )
    readonly_fields = ["image_prew", ]
    list_display = ('titolo','nome','cognome','indirizzo','citta','stato','telefono')
    search_fields = ('nome','cognome','indirizzo','citta','stato','telefono','mail')
    radio_fields = {"lingua": admin.HORIZONTAL,"genere": admin.HORIZONTAL}
    list_per_page = 25

class AutoreInline(CompactInline):
    model = Autore
    extra = 1
    show_change_link = True



class OperaAdmin(ImportExportModelAdmin):

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


    readonly_fields = ["image_prew", ]
    list_display = ('id','titolo_opera','autore','riconoscimenti','pos_arch','edizione',   'image_prew', 'abstract_','tag')
    search_fields = ('posizione_archivio','tag','titolo_opera')
    filter=('titolo_opera','autore','edizione','posizione_archivio','tag')
    list_filter = ('edizione','tag','autore',)
    list_per_page = 25






# Register your models here.
admin.site.register(Autore,AutoreAdmin)
admin.site.register(Opera,OperaAdmin)
admin.site.register(Immagini,ImmaginiAdmin)




