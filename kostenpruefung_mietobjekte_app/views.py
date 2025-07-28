from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Prefetch, Sum
from django.forms import modelformset_factory
from django.utils import timezone

from .models import Mietobjekt, Mieter, Rechnung, Rechnungsart, Lieferant, Konto, Mieteinheit, Prozent
from .forms import MietobjektForm, RechnungForm, RechnungsartForm, LieferantForm, KontoForm, MieteinheitForm, ProzentForm
from .forms import MieterObjektForm, MietverhaeltnisForm  # Remove MieterEinheitForm

# Create your views here.

def objekt_index(request):
    objekte = Mietobjekt.objects.filter(created_by=request.user)
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
    mietobjekt = Mietobjekt.objects.filter(id=mietobjekt_id, created_by=request.user).first()
    if not mietobjekt:
        return HttpResponse("Nicht erlaubt", status=403)
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
    mieter = Mieter.objects.filter(created_by=request.user)
    return render(request, 'kostenpruefung_mietobjekte_app/mieter.html', {'mieter': mieter})

def mieter_laufend(request):
    today = timezone.now().date()
    # Get all tenants who have at least one current contract
    mieter_with_current = Mieter.objects.filter(
        created_by=request.user,
        mietverhaeltnisse__vertragsbeginn__lte=today,
        mietverhaeltnisse__vertragsende__gte=today
    ).distinct().prefetch_related('mietverhaeltnisse__mietobjekte', 'mietverhaeltnisse__mieteinheiten')
    
    return render(request, 'kostenpruefung_mietobjekte_app/mieter_laufend.html', {'mieter': mieter_with_current})

def mieter_zukuenftig(request):
    today = timezone.now().date()
    # Get all tenants who have at least one future contract
    mieter_with_future = Mieter.objects.filter(
        created_by=request.user,
        mietverhaeltnisse__vertragsbeginn__gt=today
    ).distinct().prefetch_related('mietverhaeltnisse__mietobjekte', 'mietverhaeltnisse__mieteinheiten')
    
    return render(request, 'kostenpruefung_mietobjekte_app/mieter_zukuenftig.html', {'mieter': mieter_with_future})

def mieter_archiv(request):
    today = timezone.now().date()
    # Get all tenants who have at least one past contract
    mieter_with_past = Mieter.objects.filter(
        created_by=request.user,
        mietverhaeltnisse__vertragsende__lt=today
    ).distinct().prefetch_related('mietverhaeltnisse__mietobjekte', 'mietverhaeltnisse__mieteinheiten')
    
    return render(request, 'kostenpruefung_mietobjekte_app/mieter_archiv.html', {'mieter': mieter_with_past})

def mieter_create_step1(request):
    if request.method == 'POST':
        form = MieterObjektForm(request.POST)
        if form.is_valid():
            mieter = form.save(commit=False)
            mieter.created_by = request.user
            mieter.save()
            
            # Now redirect directly to create a Mietverhaeltnis for this Mieter
            return redirect('mietverhaeltnis_create', mieter_id=mieter.id)
    else:
        form = MieterObjektForm()
    return render(request, 'kostenpruefung_mietobjekte_app/mieter_objekt_form.html', {'form': form})

def rechnungen(request):
    rechnungen = Rechnung.objects.filter(created_by=request.user).prefetch_related(
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
    rechnung = Rechnung.objects.filter(id=rechnung_id, created_by=request.user).first()
    if not rechnung:
        return HttpResponse("Nicht erlaubt", status=403)
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
    kostenarten = Rechnungsart.objects.filter(created_by=request.user)
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
    lieferanten = Lieferant.objects.filter(created_by=request.user)
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
    konten = Konto.objects.filter(created_by=request.user)
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
    mietobjekte = Mietobjekt.objects.filter(created_by=request.user)
    selected_id = request.GET.get('mietobjekt')
    selected_objekt = Mietobjekt.objects.filter(id=selected_id, created_by=request.user).first() if selected_id else None

    einnahmen_sum = 0
    ausgaben_sum = 0
    chart_data = {}

    if selected_objekt:
        # Calculate Einnahmen (from Konto)
        kontos = Konto.objects.filter(mietobjekt=selected_objekt, created_by=request.user)
        for konto in kontos:
            betrag = getattr(konto, 'betrag', 0)
            if betrag > 0:  # Only include positive amounts as Einnahmen
                einnahmen_sum += betrag
                kategorie = getattr(konto, 'buchungsart', None)
                cat_name = kategorie.name if kategorie else "Sonstige"
                chart_data[cat_name] = chart_data.get(cat_name, 0) + betrag

        # Calculate Ausgaben (from Rechnung)
        rechnungen = Rechnung.objects.filter(mietobjekt=selected_objekt, created_by=request.user)
        for rechnung in rechnungen:
            ausgaben_sum += rechnung.betrag

        # Group Ausgaben by art/buchungsart
        ausgaben_by_art = (
            Rechnung.objects.filter(mietobjekt=selected_objekt, created_by=request.user)
            .values('art__name')  # Group by art name
            .annotate(total=Sum('betrag'))  # Sum up betrag for each art
        )

        # Prepare data for the pie chart
        chart_labels = [item['art__name'] for item in ausgaben_by_art]
        chart_values = [float(item['total']) for item in ausgaben_by_art]  # Convert Decimal to float

        # Group Einnahmen by art/buchungsart
        einnahmen_by_art = (
            Konto.objects.filter(mietobjekt=selected_objekt, betrag__gt=0, created_by=request.user)
            .values('buchungsart__name')  # Group by buchungsart name
            .annotate(total=Sum('betrag'))  # Sum up betrag for each buchungsart
        )

        # Prepare data for the Einnahmen pie chart
        einnahmen_labels = [item['buchungsart__name'] for item in einnahmen_by_art]
        einnahmen_values = [float(item['total']) for item in einnahmen_by_art]  # Convert Decimal to float
    ergebnis = einnahmen_sum - ausgaben_sum

    return render(request, 'kostenpruefung_mietobjekte_app/auswertung.html', {
        'mietobjekte': mietobjekte,
        'selected_objekt': selected_objekt,
        'einnahmen': einnahmen_sum,
        'ausgaben': ausgaben_sum,
        'ergebnis': ergebnis,
        'chart_labels': chart_labels if selected_objekt else [],
        'chart_values': chart_values if selected_objekt else [],
        'einnahmen_labels': einnahmen_labels if selected_objekt else [],
        'einnahmen_values': einnahmen_values if selected_objekt else [],
    })

def mietverhaeltnis_create(request, mieter_id):
    mieter = Mieter.objects.filter(id=mieter_id, created_by=request.user).first()
    if not mieter:
        return HttpResponse("Nicht erlaubt", status=403)
    
    if request.method == 'POST':
        form = MietverhaeltnisForm(request.POST)
        if form.is_valid():
            mietverhaeltnis = form.save(commit=False)
            mietverhaeltnis.mieter = mieter
            mietverhaeltnis.created_by = request.user
            mietverhaeltnis.save()
            form.save_m2m()  # Save many-to-many relationships
            
            # Determine which page to return to based on contract status
            today = timezone.now().date()
            if mietverhaeltnis.vertragsbeginn > today:
                return redirect('mieter_zukuenftig')
            elif mietverhaeltnis.vertragsende < today:
                return redirect('mieter_archiv')
            else:
                return redirect('mieter_laufend')
    else:
        form = MietverhaeltnisForm()
    
    return render(request, 'kostenpruefung_mietobjekte_app/mietverhaeltnis_form.html', {
        'form': form,
        'mieter': mieter
    })