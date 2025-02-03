# import pathurl external files
from django.urls import re_path

from Gestionale.urls.stampe_schede_anno import *
from Gestionale.viste import OperaForm as operaform
from Gestionale.viste import documents as doc
from Gestionale.viste import importload as impload
from Gestionale.viste import routine as routine
from Gestionale.viste import tesdoc as docx
from Gestionale.viste import utility as utils
from Gestionale.viste import views as mainview

app_name = 'core'


urlpatterns = [path('jet_api/', include('jet_django.urls')),
               # re_path(r'__debug__/', include("debug_toolbar.urls")),

               re_path(r'^$', mainview.home, name="home"),
               re_path(r'^login/$', mainview.login, name='login'),
               re_path(r'^logout/$', auth_views.LogoutView, name='logout'),
               re_path(r'^exportautori/', mainview.export_data_autori, name='exportautori'),
               re_path(r'^exportopere/', mainview.export_data_opere, name='exportopere'),
               re_path(r'^exportimmagini/', mainview.export_data_immagini, name='exportimmagini'),
               re_path(r'^operacompleta/$', mainview.opera_full, name='exportopera_completa'),
               re_path(r'^operelistacompleta_autori/$', mainview.opere_list_full_autori,
                      name='exportilistcompleta_autori'),


                  # elenco esportazioni
               re_path(r'^operelistacompleta/$', mainview.opere_list_full, name='exportilistcompleta'),
               re_path(r'^operelistacompletaultimo/$', mainview.opere_list_full_last, name='exportilistcompletalast'),
               re_path(r'^autorifull/$', mainview.autori_full, name='autori_full'),
               re_path(r'^backup/$', mainview.backup, name='backup'),

                  # esportazione documenti
               re_path(r'^doc/address$', mainview.adress_plaque, name='doc_address'),
               re_path(r'^doc/elenco_alfa$', mainview.elenco_alfa, name='doc_alfa'),

                  # esportazione documenti word
               re_path(r'^doc/docx/ultimaedizione', doc.main, name='docx'),
               re_path(r'^doc/docx/dati', doc.docx, name='docx_dati'),

                  # importazione documneti
               re_path(r'^importload', impload.importjsondata, name='doc-imp'),

                  # conversione imamgini anteprima
               re_path(r'^covimages$', utils.compress_images_previews, name='prev-images'),
               re_path(r'^correctprew$', utils.correct_images_previews, name='correct-prev-images'),
                  # Eliminazione caratteri problematici campi
                  path('datapurge/<str:model>/<str:field>/', utils.purgeCaracters, name='field_clean'),

                  # servizi
               re_path(r'^script/main/$', mainview.utilities, name='utilities'),  # pagina generale
               re_path(r'^script/lowcase/$', mainview.lower_case, name='lowcase'),  # rimposta i testi in minuscolo
               re_path(r'^script/mongosave/$', mainview.mongosave, name='mongosave'),  # salvataggio dati in MongoDB

               # routines
               re_path(r'^routine/tags_extract/$', routine.extract_tags, name='tag_extract'),

                  # statistic
               re_path(r'^stat/', include('Gestionale.urls.statistic'), name='statistic'),
               # salvataggio dati in MongoDB

                  #doc gernerator
               re_path(r'^doctest/', docx.document, name='documents'),  # salvataggio dati in MongoDB

               # doc gernerator
               re_path(r'^OperaForm/', operaform.insert_opera, name='opera_insert'),  # salvataggio dati in MongoDB

               ] + urlpatterns_report + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'Gestionale.viste.views.handler404'
handler500 = 'Gestionale.viste.views.handler500'
