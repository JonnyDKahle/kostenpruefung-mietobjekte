from django.urls import path
from .views import test_view, objekt_index, mieter, rechnungen, kostenarten, lieferanten



urlpatterns = [
    path('test/', test_view, name='test'),
    path('', objekt_index, name='objekt_index'),
    path('mieter/', mieter, name='mieter'),
    path('rechnungen/', rechnungen, name='rechnungen'),
    path('kostenarten/', kostenarten, name='kostenarten'),
    path('lieferanten/', lieferanten, name='lieferanten'),
]