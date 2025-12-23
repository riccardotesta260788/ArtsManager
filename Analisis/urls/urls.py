from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path

from Analisis import views as mainview

app_name = 'core'

urlpatterns = [url(r'^analisys/color/$', mainview.get_realcolor,
                   name='colorspace'),
               ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'Gestionale.viste.views.handler404'
handler500 = 'Gestionale.viste.views.handler500'
