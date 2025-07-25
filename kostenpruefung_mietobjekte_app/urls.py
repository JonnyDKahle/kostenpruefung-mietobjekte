from django.urls import path
from .views import test_view, objekt_index, mieter, rechnungen, kostenarten, lieferanten, mietobjekt_create



urlpatterns = [
    path('test/', test_view, name='test'),
    path('', objekt_index, name='objekt_index'),
    path('mietobjekt/create/', mietobjekt_create, name='mietobjekt_create'),
    path('mieter/', mieter, name='mieter'),
    path('rechnungen/', rechnungen, name='rechnungen'),
    path('kostenarten/', kostenarten, name='kostenarten'),
    path('lieferanten/', lieferanten, name='lieferanten'),
]