from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Prefetch
from django.forms import modelformset_factory
from .models import Mietobjekt, Mieter, Rechnung, Rechnungsart, Lieferant, Konto, Mieteinheit, Prozent
from .forms import MietobjektForm, RechnungForm, RechnungsartForm, LieferantForm, KontoForm, MieteinheitForm, ProzentForm
from .forms import MieterObjektForm, MieterEinheitForm

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

def mieter_create_step1(request):
    if request.method == 'POST':
        form = MieterObjektForm(request.POST)
        if form.is_valid():
            mieter = form.save(commit=False)
            mieter.created_by = request.user
            mieter.save()
            form.save_m2m()
            # Pass selected Mietobjekte IDs to next step
            mietobjekte_ids = [obj.id for obj in form.cleaned_data['mietobjekte']]
            request.session['mieter_id'] = mieter.id
            request.session['mietobjekte_ids'] = mietobjekte_ids
            return redirect('mieter_create_step2')
    else:
        form = MieterObjektForm()
    return render(request, 'kostenpruefung_mietobjekte_app/mieter_objekt_form.html', {'form': form})

def mieter_create_step2(request):
    mieter_id = request.session.get('mieter_id')
    mietobjekte_ids = request.session.get('mietobjekte_ids', [])
    mietobjekte = Mietobjekt.objects.filter(id__in=mietobjekte_ids)
    mieter = Mieter.objects.get(id=mieter_id)
    if request.method == 'POST':
        form = MieterEinheitForm(request.POST, mietobjekte=mietobjekte)
        if form.is_valid():
            mieter.mieteinheiten.set(form.cleaned_data['mieteinheiten'])
            return redirect('mieter')
    else:
        form = MieterEinheitForm(mietobjekte=mietobjekte)
    return render(request, 'kostenpruefung_mietobjekte_app/mieter_einheit_form.html', {'form': form, 'mieter': mieter})

def rechnungen(request):
    rechnungen = Rechnung.objects.prefetch_related(
        'lieferant',
        'mietobjekt__mieteinheiten__prozent_mieteinheit',
        'prozent_rechnung'
    )
    for r in rechnungen:
        total = 0
        for mieteinheit in r.mietobjekt.mieteinheiten.all():
            for prozent in mieteinheit.prozent_mieteinheit.all():
                if prozent in r.prozent_rechnung.all():
                    total += prozent.prozent or 0
        # Add a custom attribute to each Rechnung object
        r.percent_not_100 = abs(total - 100) > 0.01
    return render(request, 'kostenpruefung_mietobjekte_app/rechnungen.html', {
        'rechnungen': rechnungen,
    })

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

def auswertung(request):
    mietobjekte = Mietobjekt.objects.all()
    selected_id = request.GET.get('mietobjekt')
    selected_objekt = Mietobjekt.objects.filter(id=selected_id).first() if selected_id else None

    einnahmen_sum = 0
    ausgaben_sum = 0
    chart_data = {}

    if selected_objekt:
        # Calculate Einnahmen (from Konto, if applicable)
        kontos = Konto.objects.filter(mieter__mietobjekte=selected_objekt)
        for konto in kontos:
            betrag = getattr(konto, 'betrag', 0)
            kategorie = getattr(konto, 'buchungsart', None)
            if betrag >= 0:
                einnahmen_sum += betrag
                cat_name = kategorie.name if kategorie else "Sonstige"
                chart_data[cat_name] = chart_data.get(cat_name, 0) + betrag

        # Calculate Ausgaben (from Rechnung)
        rechnungen = Rechnung.objects.filter(mietobjekt=selected_objekt)
        for rechnung in rechnungen:
            ausgaben_sum += rechnung.betrag

    ergebnis = einnahmen_sum - ausgaben_sum

    # Prepare chart labels and values
    chart_labels = list(chart_data.keys())
    chart_values = list(chart_data.values())

    return render(request, 'kostenpruefung_mietobjekte_app/auswertung.html', {
        'mietobjekte': mietobjekte,
        'selected_objekt': selected_objekt,
        'einnahmen': einnahmen_sum,
        'ausgaben': ausgaben_sum,
        'ergebnis': ergebnis,
        'chart_labels': chart_labels,
        'chart_values': chart_values,
    })