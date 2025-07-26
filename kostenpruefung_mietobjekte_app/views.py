from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Prefetch
from django.forms import modelformset_factory
from .models import Mietobjekt, Mieter, Rechnung, Rechnungsart, Lieferant, Konto, Mieteinheit, Prozent
from .forms import MietobjektForm, RechnungForm, RechnungsartForm, LieferantForm, KontoForm, MieteinheitForm, ProzentForm

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

def mieteinheit_create(request, mietobjekt_id):
    mietobjekt = Mietobjekt.objects.get(id=mietobjekt_id)
    if request.method == 'POST':
        form = MieteinheitForm(request.POST)
        if form.is_valid():
            mieteinheit = form.save(commit=False)
            mieteinheit.mietobjekt = mietobjekt  # Prefill and hide from user
            mieteinheit.save()
            return redirect('objekt_index')
    else:
        form = MieteinheitForm()
    return render(request, 'kostenpruefung_mietobjekte_app/mieteinheit_form.html', {'form': form, 'mietobjekt': mietobjekt})

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

def prozent_bulk_update(request, rechnung_id):
    rechnung = Rechnung.objects.get(id=rechnung_id)
    mieteinheiten = rechnung.mietobjekt.mieteinheiten.all()
    ProzentFormSet = modelformset_factory(Prozent, form=ProzentForm, extra=0, can_delete=False)

    for mieteinheit in mieteinheiten:
        Prozent.objects.get_or_create(rechnung=rechnung, mieteinheit=mieteinheit)

    queryset = Prozent.objects.filter(rechnung=rechnung, mieteinheit__in=mieteinheiten)

    if request.method == 'POST':
        print("POST data:", request.POST)  # Debug: print POST data
        formset = ProzentFormSet(request.POST, queryset=queryset)
        print("Formset is valid:", formset.is_valid())  # Debug: print formset validity
        if formset.is_valid():
            instances = formset.save(commit=False)
            print("Instances to save:", instances)  # Debug: print instances
            for instance in instances:
                instance.rechnung = rechnung
                instance.save()
            formset.save_m2m()
            print("Saved successfully, redirecting.")
            return redirect('rechnungen')
        else:
            print("Formset errors:", formset.errors)  # Debug: print errors
    else:
        formset = ProzentFormSet(queryset=queryset)

    return render(request, 'kostenpruefung_mietobjekte_app/prozent_bulk_form.html', {
        'formset': formset,
        'rechnung': rechnung,
    })

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