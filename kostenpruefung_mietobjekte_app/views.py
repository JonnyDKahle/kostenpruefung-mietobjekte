from django.shortcuts import render
from django.http import HttpResponse
from .models import Mietobjekt, Mieter

# Create your views here.
def test_view(request):
    return HttpResponse("it works")

def objekt_index(request):
    objekte = Mietobjekt.objects.all()
    return render(request, 'kostenpruefung_mietobjekte_app/objekt_index.html', {'objekte': objekte})

def mieter(request):
    mieter = Mieter.objects.all()
    return render(request, 'kostenpruefung_mietobjekte_app/mieter.html', {'mieter': mieter})