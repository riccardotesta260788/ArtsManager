from django.conf.urls import url,include
from django.conf import settings
from Gestionale.viste import statistica as stat

app_name='statistic'
urlpatterns = [

#statistic
    url(r'^pie_eta/$', stat.get_eta, name='pie_eta'), #Estrazione composizione campione eta

]