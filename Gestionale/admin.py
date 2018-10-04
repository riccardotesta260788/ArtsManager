from django.contrib import admin
from django import forms

from .models import *
from django.contrib.admin import AdminSite
from Gestionale import views as mainview
from simple_history.admin import SimpleHistoryAdmin
from jet.admin import CompactInline


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



class ImmaginiAdmin(admin.ModelAdmin):


    def image_prew(self, obj):
        return mark_safe('<img src="/media/{0}" style="max-width:150px;height:auto">'.format(obj.imagefile))

    readonly_fields = ["image_prew","metainfo" ]
    list_display = ('titolo',"image_meta_","image_prew")
    search_fields = ('titolo',)
    list_filter=('titolo',)
    list_per_page = 25

    fieldsets = [
        (None, {'fields': ['titolo']}),
        ('Immagini', {'fields': ['imagefile','imagefile1','imagefile2']}),
    ]

class AutoreAdmin(admin.ModelAdmin):


    def image_prew(self, obj):
        return mark_safe('<img src="/media/{0}" style="max-width:150px;height:auto">'.format(obj.imagefile)
                     )
    readonly_fields = ["image_prew", ]
    list_display = ('titolo','nome','cognome','indirizzo','citta','stato','telefono','history')
    search_fields = ('nome','cognome','indirizzo','citta','stato','telefono','mail')
    radio_fields = {"lingua": admin.HORIZONTAL,"genere": admin.HORIZONTAL}
    list_per_page = 25

class AutoreInline(CompactInline):
    model = Autore
    extra = 1
    show_change_link = True



class OperaAdmin(admin.ModelAdmin):

    def image_prew(self, obj):
        return mark_safe('<a href="/media/{0}" target="_blank"><img src="/media/{0}" style="max-width:150px;height:auto"></a>'.format(obj.immagini.imagefile))
    readonly_fields = ["image_prew", ]
    list_display = ('indicazione_', 'titolo_opera', 'autore', 'image_prew', 'abstract_','tag')
    search_fields = ('titolo_opera','tag')
    list_per_page = 25






# Register your models here.
admin.site.register(Autore,AutoreAdmin)
admin.site.register(Opera,OperaAdmin)
admin.site.register(Immagini,ImmaginiAdmin)




