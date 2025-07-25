from django.urls import path
from .views import (objekt_index, mieter, rechnungen, kostenarten, lieferanten, konto, mieter_create_step1, 
                    mieter_create_step2)
from .views import mietobjekt_create, rechnung_create, rechnungsart_create, lieferant_create, konto_create
from .views import mieteinheit_create, prozent_bulk_update



urlpatterns = [
    path('', objekt_index, name='objekt_index'),
    path('mietobjekt/create/', mietobjekt_create, name='mietobjekt_create'),
    path('mieteinheit/create/<int:mietobjekt_id>/', mieteinheit_create, name='mieteinheit_create'),
    path('mieter/', mieter, name='mieter'),
    path('mieter/create/step1/', mieter_create_step1, name='mieter_create_step1'),
    path('mieter/create/step2/', mieter_create_step2, name='mieter_create_step2'),
    path('rechnungen/', rechnungen, name='rechnungen'),
    path('rechnung/create/', rechnung_create, name='rechnung_create'),
    path('prozent/bulk_update/<int:rechnung_id>/', prozent_bulk_update, name='prozent_bulk_update'),
    path('kostenarten/', kostenarten, name='kostenarten'),
    path('rechnungsart/create/', rechnungsart_create, name='rechnungsart_create'),
    path('lieferanten/', lieferanten, name='lieferanten'),
    path('lieferant/create/', lieferant_create, name='lieferant_create'),
    path('konto/', konto, name='konto'),
    path('konto/create/', konto_create, name='konto_create'),
]