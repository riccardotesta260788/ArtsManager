from django.contrib import admin
from .models import *


admin.site.site_header ="Binneale Incisione - Admin"
admin.site.site_title = "Binneale Incisione Portal"
admin.site.index_title = "Benvenuti sul portale della Binneale di Incisione"



class ImmaginiAdmin(admin.ModelAdmin):


    def image_prew(self, obj):
        return mark_safe('<img src="/media/{0}" style="max-width:150px;height:auto">'.format(obj.imagefile)
                     )
    readonly_fields = ["image_prew", ]
    list_display = ('titolo_opera',"image_meta_","image_prew",)
    search_fields = ('titolo_opera',)
    list_per_page = 25



class OperaAdmin(admin.ModelAdmin):


    def image_prew(self, obj):
        return mark_safe('<a href="/media/{0}" target="_blank"><img src="/media/{0}" style="max-width:150px;height:auto"></a>'.format(obj.immagini.imagefile))
    readonly_fields = ["image_prew", ]
    list_display = ('indicazione_', 'titolo_opera', 'autore', 'image_prew', 'abstract_')
    search_fields = ('indicazione_',)
    list_per_page = 25


class AutoreAdmin(admin.ModelAdmin):


    def image_prew(self, obj):
        return mark_safe('<img src="/media/{0}" style="max-width:150px;height:auto">'.format(obj.imagefile)
                     )
    readonly_fields = ["image_prew", ]
    list_display = ('titolo','nome','cognome','indirizzo','citta','stato','telefono',"image_prew")
    search_fields = ('nome','cognome','indirizzo','citta','stato','telefono','mail')
    radio_fields = {"lingua": admin.HORIZONTAL,"genere": admin.HORIZONTAL}
    list_per_page = 25


# Register your models here.
admin.site.register(Autore,AutoreAdmin)
admin.site.register(Opera,OperaAdmin)
admin.site.register(Immagini,ImmaginiAdmin)



