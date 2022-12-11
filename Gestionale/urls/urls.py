from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path

from Gestionale.viste import documents as doc
from Gestionale.viste import importload as impload
from Gestionale.viste import tesdoc as docx
from Gestionale.viste import utility as utils
from Gestionale.viste import views as mainview

app_name = 'core'


urlpatterns = [path('jet_api/', include('jet_django.urls')),

                  url(r'^$', mainview.home, name="home"),
                  url(r'^login/$', mainview.login, name='login'),
                  url(r'^logout/$', auth_views.LogoutView, name='logout'),
                  url(r'^exportautori/', mainview.export_data_autori, name='exportautori'),
                  url(r'^exportopere/', mainview.export_data_opere, name='exportopere'),
                  url(r'^exportimmagini/', mainview.export_data_immagini, name='exportimmagini'),
                  url(r'^operacompleta/$', mainview.opera_full, name='exportopera_completa'),
                  url(r'^operelistacompleta_autori/$', mainview.opere_list_full_autori,
                      name='exportilistcompleta_autori'),


                  # elenco esportazioni
                  url(r'^operelistacompleta/$', mainview.opere_list_full, name='exportilistcompleta'),
                  url(r'^operelistacompletaultimo/$', mainview.opere_list_full_last, name='exportilistcompletalast'),
                  url(r'^autorifull/$', mainview.autori_full, name='autori_full'),
                  url(r'^backup/$', mainview.backup, name='backup'),

                  # esportazione documenti
                  url(r'^doc/address$', mainview.adress_plaque, name='doc_address'),
                  url(r'^doc/elenco_alfa$', mainview.elenco_alfa, name='doc_alfa'),

                  # esportazione documenti word
                  url(r'^doc/docx/ultimaedizione', doc.main, name='docx'),
                  url(r'^doc/docx/dati', doc.docx, name='docx_dati'),

                  # importazione documneti
                  url(r'^importload$', impload.importjsondata, name='doc-imp'),
                  # conversione imamgini anteprima
                  url(r'^covimages$', utils.compress_images_previews, name='prev-images'),
                  url(r'^correctprew$', utils.correct_images_previews, name='correct-prev-images'),
                  # Eliminazione caratteri problematici campi
                  path('datapurge/<str:model>/<str:field>/', utils.purgeCaracters, name='field_clean'),

                  # servizi
                  url(r'^script/main/$', mainview.utilities, name='utilities'),  # pagina generale
                  url(r'^script/lowcase/$', mainview.lower_case, name='lowcase'),  # rimposta i testi in minuscolo
                  url(r'^script/mongosave/$', mainview.mongosave, name='mongosave'),  # salvataggio dati in MongoDB

                  # statistic
                  url(r'^stat/', include('Gestionale.urls.statistic'), name='statistic'),  # salvataggio dati in MongoDB

                  #doc gernerator
                  url(r'^doctest/', docx.document, name='documents'),  # salvataggio dati in MongoDB


              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'Gestionale.viste.views.handler404'
handler500 = 'Gestionale.viste.views.handler500'
