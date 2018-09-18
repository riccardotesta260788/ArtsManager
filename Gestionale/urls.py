from django.conf.urls import url,include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from Gestionale import views as mainview
from django.contrib.auth import views as auth_views



urlpatterns = [
    url(r'^$',mainview.home,name="home"),
    url(r'^login/$', mainview.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^exportautori/', mainview.export_data_autori , name='exportautori'),
    url(r'^exportopere/', mainview.export_data_opere , name='exportopere'),
    url(r'^exportimmagini/', mainview.export_data_immagini , name='exportimmagini'),
    url(r'^operacompleta/$', mainview.opera_full , name='exportimmagini'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 ='Gestionale.views.handler404'
handler500 ='Gestionale.views.handler500'