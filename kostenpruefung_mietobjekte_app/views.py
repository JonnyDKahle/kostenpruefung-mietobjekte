from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Mietobjekt, Mieter, Rechnung, Rechnungsart, Lieferant
from .forms import MietobjektForm, RechnungForm

# Create your views here.

def objekt_index(request):
    objekte = Mietobjekt.objects.all()
    return render(request, 'kostenpruefung_mietobjekte_app/objekt_index.html', {'objekte': objekte})

def mietobjekt_create(request):
    if request.method == 'POST':
        form = MietobjektForm(request.POST)
        if form.is_valid():
            mietobjekt = form.save(commit=False)
            mietobjekt.created_by = request.user
            mietobjekt.save()
            return redirect('objekt_index')
    else:
        form = MietobjektForm()
    return render(request, 'kostenpruefung_mietobjekte_app/mietobjekt_form.html', {'form': form})

def mieter(request):
    mieter = Mieter.objects.all()
    return render(request, 'kostenpruefung_mietobjekte_app/mieter.html', {'mieter': mieter})

def rechnungen(request):
    rechnungen = Rechnung.objects.all()
    return render(request, 'kostenpruefung_mietobjekte_app/rechnungen.html', {'rechnungen': rechnungen})

def rechnung_create(request):
    if request.method == 'POST':
        form = RechnungForm(request.POST)
        if form.is_valid():
            rechnung = form.save(commit=False)
            rechnung.created_by = request.user
            rechnung.save()
            form.save_m2m()
            return redirect('rechnungen')
    else:
        form = RechnungForm()
    return render(request, 'kostenpruefung_mietobjekte_app/rechnung_form.html', {'form': form})

def kostenarten(request):
    kostenarten = Rechnungsart.objects.all()
    return render(request, 'kostenpruefung_mietobjekte_app/kostenarten.html', {'kostenarten': kostenarten})

def lieferanten(request):
    lieferanten = Lieferant.objects.all()
    return render(request, 'kostenpruefung_mietobjekte_app/lieferant.html', {'lieferanten': lieferanten})