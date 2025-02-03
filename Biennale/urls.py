"""Biennale URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, re_path

admin.autodiscover()

'''OLD Python2.7
'''
# urlpatterns = [
#
#     url(r'admin/doc/',include('django.contrib.admindocs.urls')),
#     re_path(r'admin/', admin.site.urls),
#     url(r'accounts/', include('django.contrib.auth.urls')),
#     url(r'async_include/', include('async_include.urls', namespace="async_include")),
#     url(r'^', include('Gestionale.urls.urls')),
#     url(r'^', include('Analisis.urls.urls')), #Urls per la gestione delle attività di routine
#
#
#     # url(r'^jet/', include('jet.urls', 'jet')),  # Django JET URLS
#     # url(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),  # Django JET dashboard URLS
# ]

urlpatterns = [

    re_path(r'admin/doc/', include('django.contrib.admindocs.urls')),
    re_path(r'admin/', admin.site.urls),
    re_path(r'accounts/', include('django.contrib.auth.urls')),
    re_path(r'async_include/', include('async_include.urls', namespace="async_include")),
    re_path(r'^', include('Gestionale.urls.urls')),
    re_path(r'^', include('Analisis.urls.urls')),  # Urls per la gestione delle attività di routine


    # url(r'^jet/', include('jet.urls', 'jet')),  # Django JET URLS
    # url(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),  # Django JET dashboard URLS
]


handler404 ='Gestionale.views.handler404'
handler500 ='Gestionale.views.handler500'