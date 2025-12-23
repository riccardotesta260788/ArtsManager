from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from django.urls import path

from ..viste.stampe import schede_anno as schedeanno

app_name = 'core'

urlpatterns_report = [path('report_autori_anno/<int:year>/', schedeanno.opere_anno_list_full, name="report_anno"),

                      ]
