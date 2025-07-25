from django.urls import path
from .views import objekt_index, mieter, rechnungen, kostenarten, lieferanten, konto
from .views import mietobjekt_create, rechnung_create, rechnungsart_create, lieferant_create



urlpatterns = [
    path('', objekt_index, name='objekt_index'),
    path('mietobjekt/create/', mietobjekt_create, name='mietobjekt_create'),
    path('mieter/', mieter, name='mieter'),
    path('rechnungen/', rechnungen, name='rechnungen'),
    path('rechnung/create/', rechnung_create, name='rechnung_create'),
    path('kostenarten/', kostenarten, name='kostenarten'),
    path('rechnungsart/create/', rechnungsart_create, name='rechnungsart_create'),
    path('lieferanten/', lieferanten, name='lieferanten'),
    path('lieferant/create/', lieferant_create, name='lieferant_create'),
    path('konto/', konto, name='konto'),
]