from django.conf.urls import url,include
from django.conf import settings
from django.conf.urls.static import static
from Gestionale.viste import views as mainview
from django.contrib.auth import views as auth_views

app_name='core'

urlpatterns = [
    url(r'^$',mainview.home,name="home"),
    url(r'^login/$', mainview.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^exportautori/', mainview.export_data_autori , name='exportautori'),
    url(r'^exportopere/', mainview.export_data_opere , name='exportopere'),
    url(r'^exportimmagini/', mainview.export_data_immagini , name='exportimmagini'),
    url(r'^operacompleta/$', mainview.opera_full , name='exportopera_completa'),
    url(r'^operelistacompleta_autori/$', mainview.opere_list_full_autori , name='exportilistcompleta_autori'),
    url(r'^operelistacompleta/$', mainview.opere_list_full , name='exportilistcompleta'),
    url(r'^autorifull/$', mainview.autori_full , name='autori_full'),
    url(r'^backup/$', mainview.backup , name='backup'),

#esportazione documenti
    url(r'^doc/address$', mainview.adress_plaque, name='doc_address'),
    url(r'^doc/elenco_alfa$', mainview.elenco_alfa, name='doc_alfa'),

#servizi
    url(r'^script/main/$', mainview.utilities , name='utilities'), #pagina generale
    url(r'^script/lowcase/$', mainview.lower_case , name='lowcase'), #rimposta i testi in minuscolo
    url(r'^script/mongosave/$', mainview.mongosave , name='mongosave'), #salvataggio dati in MongoDB

#statistic
    url(r'^stat/', include('Gestionale.urls.statistic') , name='statistic'), #salvataggio dati in MongoDB

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 ='Gestionale.views.handler404'
handler500 ='Gestionale.views.handler500'