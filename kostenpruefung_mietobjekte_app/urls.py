from django.urls import path
from .views import objekt_index, mieter, rechnungen, kostenarten, lieferanten
from .views import mietobjekt_create, rechnung_create



urlpatterns = [
    path('', objekt_index, name='objekt_index'),
    path('mietobjekt/create/', mietobjekt_create, name='mietobjekt_create'),
    path('mieter/', mieter, name='mieter'),
    path('rechnungen/', rechnungen, name='rechnungen'),
    path('rechnung/create/', rechnung_create, name='rechnung_create'),
    path('kostenarten/', kostenarten, name='kostenarten'),
    path('lieferanten/', lieferanten, name='lieferanten'),
]