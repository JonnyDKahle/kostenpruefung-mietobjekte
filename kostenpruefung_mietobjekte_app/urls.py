from django.urls import path
from .views import test_view, objekt_index, mieter



urlpatterns = [
    path('test/', test_view, name='test'),
    path('', objekt_index, name='objekt_index'),
    path('mieter/', mieter, name='mieter'),
]