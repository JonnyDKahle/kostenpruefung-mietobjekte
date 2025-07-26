from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Prefetch
from .models import Mietobjekt, Mieter, Rechnung, Rechnungsart, Lieferant, Konto
from .forms import MietobjektForm, RechnungForm, RechnungsartForm, LieferantForm, KontoForm

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
    rechnungen = Rechnung.objects.prefetch_related(
        'lieferant',
        'mietobjekt__mieteinheiten__prozent_mieteinheit'
    )
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

def rechnungsart_create(request):
    if request.method == 'POST':
        form = RechnungsartForm(request.POST)
        if form.is_valid():
            rechnungsart = form.save(commit=False)
            rechnungsart.created_by = request.user
            rechnungsart.save()
            return redirect('kostenarten')
    else:
        form = RechnungsartForm()
    return render(request, 'kostenpruefung_mietobjekte_app/rechnungsart_form.html', {'form': form})

def lieferanten(request):
    lieferanten = Lieferant.objects.all()
    return render(request, 'kostenpruefung_mietobjekte_app/lieferant.html', {'lieferanten': lieferanten})

def lieferant_create(request):
    if request.method == 'POST':
        form = LieferantForm(request.POST)
        if form.is_valid():
            lieferant = form.save(commit=False)
            lieferant.created_by = request.user
            lieferant.save()
            return redirect('lieferanten')
    else:
        form = LieferantForm()
    return render(request, 'kostenpruefung_mietobjekte_app/lieferant_form.html', {'form': form})

def konto(request):
    konten = Konto.objects.all()
    return render(request, 'kostenpruefung_mietobjekte_app/konto.html', {'konten': konten})

def konto_create(request):
    if request.method == 'POST':
        form = KontoForm(request.POST)
        if form.is_valid():
            konto = form.save(commit=False)
            konto.created_by = request.user
            konto.save()
            form.save_m2m()
            return redirect('konto')
    else:
        form = KontoForm()
    return render(request, 'kostenpruefung_mietobjekte_app/konto_form.html', {'form': form})