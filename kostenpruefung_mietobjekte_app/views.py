# ═══════════════════════════════════════════════════════════════════════════════
# █████████████████████████ DJANGO IMPORTS & SETUP ████████████████████████████
# ═══════════════════════════════════════════════════════════════════════════════

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Prefetch, Sum
from django.forms import modelformset_factory
from django.utils import timezone
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# ═══════════════════════════════════════════════════════════════════════════════
# ██████████████████████████ LOCAL IMPORTS ████████████████████████████████████
# ═══════════════════════════════════════════════════════════════════════════════

from .models import Mietobjekt, Mieter, Rechnung, Rechnungsart, Lieferant, Konto, Mieteinheit, Prozent, Mietverhaeltnis
from .forms import MietobjektForm, RechnungForm, RechnungsartForm, LieferantForm, KontoForm, MieteinheitForm, ProzentForm
from .forms import MieterObjektForm, MietverhaeltnisForm, PasswordConfirmationForm


# ═══════════════════════════════════════════════════════════════════════════════
# ███████████████████████ MIETOBJEKT VIEWS ████████████████████████████████████
# ═══════════════════════════════════════════════════════════════════════════════

@login_required
def objekt_index(request):
    objekte = Mietobjekt.objects.filter(created_by=request.user)
    return render(request, 'kostenpruefung_mietobjekte_app/objekt_index.html', {'objekte': objekte})

@login_required
def mietobjekt_create(request):
    if request.method == 'POST':
        form = MietobjektForm(request.POST)
        if form.is_valid():
            mietobjekt = form.save(commit=False)
            mietobjekt.created_by = request.user
            mietobjekt.save()
            return redirect('kostenpruefung_mietobjekte_app:objekt_index')
    else:
        form = MietobjektForm()
    return render(request, 'kostenpruefung_mietobjekte_app/mietobjekt_form.html', {'form': form})

@login_required
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
            return redirect('kostenpruefung_mietobjekte_app:objekt_index')
    else:
        form = MieteinheitForm()
    return render(request, 'kostenpruefung_mietobjekte_app/mieteinheit_form.html', {'form': form, 'mietobjekt': mietobjekt})


# ═══════════════════════════════════════════════════════════════════════════════
# ████████████████████████████ MIETER VIEWS ███████████████████████████████████
# ═══════════════════════════════════════════════════════════════════════════════

@login_required
def mieter(request):
    mieter = Mieter.objects.filter(created_by=request.user)
    return render(request, 'kostenpruefung_mietobjekte_app/mieter.html', {'mieter': mieter})

@login_required
def mieter_laufend(request):
    today = timezone.now().date()
    
    # Get tenants with at least one current contract
    mieter_with_current = Mieter.objects.filter(
        created_by=request.user,
        mietverhaeltnisse__vertragsbeginn__lte=today,
        mietverhaeltnisse__vertragsende__gte=today
    ).distinct().prefetch_related(
        Prefetch(
            'mietverhaeltnisse',
            queryset=Mietverhaeltnis.objects.filter(
                vertragsbeginn__lte=today,
                vertragsende__gte=today
            ).prefetch_related('mietobjekte', 'mieteinheiten')
        )
    )
    
    # Get mieter without any Mietverhaeltnis
    mieter_without_mietverhaeltnis = Mieter.objects.filter(
        created_by=request.user
    ).exclude(
        mietverhaeltnisse__isnull=False
    )
    
    return render(request, 'kostenpruefung_mietobjekte_app/mieter_laufend.html', {
        'mieter': mieter_with_current,
        'mieter_without_mietverhaeltnis': mieter_without_mietverhaeltnis
    })

@login_required
def mieter_zukuenftig(request):
    today = timezone.now().date()
    
    # Get tenants with at least one future contract
    mieter_with_future = Mieter.objects.filter(
        created_by=request.user,
        mietverhaeltnisse__vertragsbeginn__gt=today
    ).distinct().prefetch_related(
        # Only prefetch FUTURE lease contracts
        Prefetch(
            'mietverhaeltnisse',
            queryset=Mietverhaeltnis.objects.filter(
                vertragsbeginn__gt=today
            ).prefetch_related('mietobjekte', 'mieteinheiten')
        )
    )
    
    # Get mieter without any Mietverhaeltnis
    mieter_without_mietverhaeltnis = Mieter.objects.filter(
        created_by=request.user
    ).exclude(
        mietverhaeltnisse__isnull=False
    )
    
    return render(request, 'kostenpruefung_mietobjekte_app/mieter_zukuenftig.html', {
        'mieter': mieter_with_future,
        'mieter_without_mietverhaeltnis': mieter_without_mietverhaeltnis
    })

@login_required
def mieter_archiv(request):
    today = timezone.now().date()
    
    # Get tenants with at least one past contract
    mieter_with_past = Mieter.objects.filter(
        created_by=request.user,
        mietverhaeltnisse__vertragsende__lt=today
    ).distinct().prefetch_related(
        # Only prefetch PAST lease contracts
        Prefetch(
            'mietverhaeltnisse',
            queryset=Mietverhaeltnis.objects.filter(
                vertragsende__lt=today
            ).prefetch_related('mietobjekte', 'mieteinheiten')
        )
    )
    
    # Get mieter without any Mietverhaeltnis
    mieter_without_mietverhaeltnis = Mieter.objects.filter(
        created_by=request.user
    ).exclude(
        mietverhaeltnisse__isnull=False
    )
    
    return render(request, 'kostenpruefung_mietobjekte_app/mieter_archiv.html', {
        'mieter': mieter_with_past,
        'mieter_without_mietverhaeltnis': mieter_without_mietverhaeltnis
    })

@login_required
def mieter_create_step1(request):
    if request.method == 'POST':
        form = MieterObjektForm(request.POST)
        if form.is_valid():
            mieter = form.save(commit=False)
            mieter.created_by = request.user
            mieter.save()
            
            # Redirect back to the mieter_laufend page instead of mietverhaeltnis_create
            return redirect('kostenpruefung_mietobjekte_app:mieter_laufend')
    else:
        form = MieterObjektForm()
    return render(request, 'kostenpruefung_mietobjekte_app/mieter_objekt_form.html', {'form': form})


# ═══════════════════════════════════════════════════════════════════════════════
# ███████████████████████ RECHNUNG VIEWS ██████████████████████████████████████
# ═══════════════════════════════════════════════════════════════════════════════

@login_required
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

@login_required
def rechnung_create(request):
    if request.method == 'POST':
        form = RechnungForm(request.POST)
        if form.is_valid():
            rechnung = form.save(commit=False)
            rechnung.created_by = request.user
            rechnung.save()
            form.save_m2m()
            return redirect('kostenpruefung_mietobjekte_app:rechnungen')
    else:
        form = RechnungForm()
    return render(request, 'kostenpruefung_mietobjekte_app/rechnung_form.html', {'form': form})

@login_required
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
            return redirect('kostenpruefung_mietobjekte_app:rechnungen')
        else:
            print("Formset errors:", formset.errors)  # Debug: print errors
    else:
        formset = ProzentFormSet(queryset=queryset)

    return render(request, 'kostenpruefung_mietobjekte_app/prozent_bulk_form.html', {
        'formset': formset,
        'rechnung': rechnung,
    })


# ═══════════════════════════════════════════════════════════════════════════════
# ██████████████████████ RECHNUNGSART VIEWS ███████████████████████████████████
# ═══════════════════════════════════════════════════════════════════════════════

@login_required
def kostenarten(request):
    kostenarten = Rechnungsart.objects.filter(created_by=request.user)
    return render(request, 'kostenpruefung_mietobjekte_app/kostenarten.html', {'kostenarten': kostenarten})

@login_required
def rechnungsart_create(request):
    if request.method == 'POST':
        form = RechnungsartForm(request.POST)
        if form.is_valid():
            rechnungsart = form.save(commit=False)
            rechnungsart.created_by = request.user
            rechnungsart.save()
            return redirect('kostenpruefung_mietobjekte_app:kostenarten')
    else:
        form = RechnungsartForm()
    return render(request, 'kostenpruefung_mietobjekte_app/rechnungsart_form.html', {'form': form})


# ═══════════════════════════════════════════════════════════════════════════════
# ███████████████████████ LIEFERANT VIEWS ██████████████████████████████████████
# ═══════════════════════════════════════════════════════════════════════════════

@login_required
def lieferanten(request):
    lieferanten = Lieferant.objects.filter(created_by=request.user)
    return render(request, 'kostenpruefung_mietobjekte_app/lieferant.html', {'lieferanten': lieferanten})

@login_required
def lieferant_create(request):
    if request.method == 'POST':
        form = LieferantForm(request.POST)
        if form.is_valid():
            lieferant = form.save(commit=False)
            lieferant.created_by = request.user
            lieferant.save()
            return redirect('kostenpruefung_mietobjekte_app:lieferanten')
    else:
        form = LieferantForm()
    return render(request, 'kostenpruefung_mietobjekte_app/lieferant_form.html', {'form': form})


# ═══════════════════════════════════════════════════════════════════════════════
# ████████████████████████ KONTO VIEWS █████████████████████████████████████████
# ═══════════════════════════════════════════════════════════════════════════════

@login_required
def konto(request):
    konten = Konto.objects.filter(created_by=request.user)
    return render(request, 'kostenpruefung_mietobjekte_app/konto.html', {'konten': konten})

@login_required
def konto_create(request):
    if request.method == 'POST':
        form = KontoForm(request.POST)
        if form.is_valid():
            konto = form.save(commit=False)
            konto.created_by = request.user
            konto.save()
            form.save_m2m()
            return redirect('kostenpruefung_mietobjekte_app:konto')
    else:
        form = KontoForm()
    return render(request, 'kostenpruefung_mietobjekte_app/konto_form.html', {'form': form})


# ═══════════════════════════════════════════════════════════════════════════════
# ██████████████████████ AUSWERTUNG VIEWS ██████████████████████████████████████
# ═══════════════════════════════════════════════════════════════════════════════

@login_required
def auswertung(request):
    import datetime
    from django.db.models import Q

    mietobjekte = Mietobjekt.objects.filter(created_by=request.user)
    selected_id = request.GET.get('mietobjekt')
    selected_objekt = Mietobjekt.objects.filter(id=selected_id, created_by=request.user).first() if selected_id else None

    # Get time filter parameters
    time_filter = request.GET.get('time_filter', 'current_year')  # Default to current year
    
    # Initialize date range variables
    start_date = None
    end_date = None
    filter_display = "Unbekannt"
    
    # Get current date info
    today = datetime.date.today()
    current_year = today.year
    last_year = current_year - 1
    
    # Available years for dropdown (from 5 years ago to current year)
    available_years = list(range(current_year - 5, current_year + 1))
    available_years.reverse()

    # Dropdown has the curent year selected as default
    try:
        selected_year = int(request.GET.get('year', current_year))
    except (ValueError, TypeError):
        selected_year = current_year
    
    # Set date range based on time filter
    if time_filter == 'current_year':
        start_date = datetime.date(current_year, 1, 1)
        end_date = datetime.date(current_year, 12, 31)
        filter_display = f"Aktuelles Jahr ({current_year})"
    
    elif time_filter == 'last_year':
        start_date = datetime.date(last_year, 1, 1)
        end_date = datetime.date(last_year, 12, 31)
        filter_display = f"Letztes Jahr ({last_year})"
    
    elif time_filter == 'total':
        # No date filtering
        filter_display = "Gesamter Zeitraum"
    
    elif time_filter == 'month_year':
        selected_month = int(request.GET.get('month', today.month))
        selected_year = int(request.GET.get('year', current_year))
        
        # Get the last day of the selected month
        if selected_month == 12:
            last_day = 31
        else:
            last_day = (datetime.date(selected_year, selected_month + 1, 1) - datetime.timedelta(days=1)).day
        
        start_date = datetime.date(selected_year, selected_month, 1)
        end_date = datetime.date(selected_year, selected_month, last_day)
        
        # Month name for display
        month_names = ["Januar", "Februar", "März", "April", "Mai", "Juni", 
                       "Juli", "August", "September", "Oktober", "November", "Dezember"]
        filter_display = f"{month_names[selected_month-1]} {selected_year}"
    
    elif time_filter == 'custom_range':
        try:
            start_date_str = request.GET.get('start_date')
            end_date_str = request.GET.get('end_date')
            
            if start_date_str:
                start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d').date()
            
            if end_date_str:
                end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d').date()
            
            if start_date and end_date:
                filter_display = f"Von {start_date.strftime('%d.%m.%Y')} bis {end_date.strftime('%d.%m.%Y')}"
            else:
                # Default to current year if invalid dates
                start_date = datetime.date(current_year, 1, 1)
                end_date = datetime.date(current_year, 12, 31)
                filter_display = f"Aktuelles Jahr ({current_year})"
        except (ValueError, TypeError):
            # Handle invalid date format
            start_date = datetime.date(current_year, 1, 1)
            end_date = datetime.date(current_year, 12, 31)
            filter_display = f"Aktuelles Jahr ({current_year})"

    einnahmen_sum = 0
    ausgaben_sum = 0
    chart_labels = []
    chart_values = []
    chart_colors = []  # Initialize chart_colors
    einnahmen_labels = []
    einnahmen_values = []
    einnahmen_colors = []  # Initialize einnahmen_colors

    if selected_objekt:
        # Date filter conditions
        date_filter = Q()
        if start_date and end_date and time_filter != 'total':
            konto_date_filter = Q(buchungstag__gte=start_date) & Q(buchungstag__lte=end_date)
            rechnung_date_filter = Q(datum__gte=start_date) & Q(datum__lte=end_date)
        else:
            konto_date_filter = Q()
            rechnung_date_filter = Q()
            
        # Calculate Einnahmen (from Konto)
        kontos = Konto.objects.filter(
            mietobjekt=selected_objekt, 
            created_by=request.user,
            betrag__gt=0
        ).filter(konto_date_filter)
        
        for konto in kontos:
            einnahmen_sum += konto.betrag

        # Calculate Ausgaben (from Rechnung)
        rechnungen = Rechnung.objects.filter(
            mietobjekt=selected_objekt, 
            created_by=request.user
        ).filter(rechnung_date_filter)
        
        for rechnung in rechnungen:
            ausgaben_sum += rechnung.betrag

        # Group Ausgaben by art/buchungsart with date filter and get colors
        ausgaben_by_art = (
            Rechnung.objects.filter(
                mietobjekt=selected_objekt, 
                created_by=request.user
            ).filter(rechnung_date_filter)
            .values('art__name', 'art__farbe')  # Include color in the query
            .annotate(total=Sum('betrag'))
        )

        # Prepare data for the pie chart with custom colors
        chart_labels = [item['art__name'] or "Ohne Kategorie" for item in ausgaben_by_art]
        chart_values = [float(item['total']) for item in ausgaben_by_art]
        chart_colors = [item['art__farbe'] or '#4e79a7' for item in ausgaben_by_art]  # Use custom colors

        # Group Einnahmen by buchungsart with date filter and get colors
        einnahmen_by_art = (
            Konto.objects.filter(
                mietobjekt=selected_objekt, 
                betrag__gt=0, 
                created_by=request.user
            ).filter(konto_date_filter)
            .values('buchungsart__name', 'buchungsart__farbe')  # Include color
            .annotate(total=Sum('betrag'))
        )

        # Prepare data for the Einnahmen pie chart with custom colors
        einnahmen_labels = [item['buchungsart__name'] or "Ohne Kategorie" for item in einnahmen_by_art]
        einnahmen_values = [float(item['total']) for item in einnahmen_by_art]
        einnahmen_colors = [item['buchungsart__farbe'] or '#4e79a7' for item in einnahmen_by_art]
    
    ergebnis = einnahmen_sum - ausgaben_sum

    return render(request, 'kostenpruefung_mietobjekte_app/auswertung.html', {
        'mietobjekte': mietobjekte,
        'selected_objekt': selected_objekt,
        'einnahmen': einnahmen_sum,
        'ausgaben': ausgaben_sum,
        'ergebnis': ergebnis,
        'chart_labels': chart_labels,
        'chart_values': chart_values,
        'chart_colors': chart_colors,  # Add colors to template context
        'einnahmen_labels': einnahmen_labels,
        'einnahmen_values': einnahmen_values,
        'einnahmen_colors': einnahmen_colors,  # Add colors to template context
        'time_filter': time_filter,
        'filter_display': filter_display,
        'start_date': start_date,
        'end_date': end_date,
        'month': request.GET.get('month', str(today.month)),
        'year': selected_year,
        'available_years': available_years,
    })


# ═══════════════════════════════════════════════════════════════════════════════
# ████████████████████ MIETVERHAELTNIS VIEWS ███████████████████████████████████
# ═══════════════════════════════════════════════════════════════════════════════

@login_required
def mietverhaeltnis_create(request, mieter_id):
    mieter = Mieter.objects.filter(id=mieter_id, created_by=request.user).first()
    if not mieter:
        return HttpResponse("Nicht erlaubt", status=403)
    
    initial_data = {}
    selected_mietobjekt = None
    
    # Check if we're updating the form with address from selected Mietobjekt
    if request.method == 'GET' and 'primary_mietobjekt' in request.GET:
        mietobjekt_id = request.GET.get('primary_mietobjekt')
        if mietobjekt_id:
            selected_mietobjekt = Mietobjekt.objects.filter(
                id=mietobjekt_id, created_by=request.user
            ).first()
            if selected_mietobjekt:
                # Pre-populate address fields
                initial_data = {
                    'strasse_hausnummer': selected_mietobjekt.strasse_hausnummer,
                    'plz': selected_mietobjekt.plz,
                    'ort': selected_mietobjekt.ort,
                    'land': selected_mietobjekt.land,
                    'primary_mietobjekt': selected_mietobjekt.id,
                    # Pre-select this in the mietobjekte field too
                    'mietobjekte': [selected_mietobjekt.id]
                }
    
    if request.method == 'POST':
        # Handle final form submission
        form = MietverhaeltnisForm(request.POST, user=request.user)
        if form.is_valid():
            mietverhaeltnis = form.save(commit=False)
            mietverhaeltnis.mieter = mieter
            mietverhaeltnis.created_by = request.user
            mietverhaeltnis.save()
            form.save_m2m()
            
            # Redirect based on contract status
            today = timezone.now().date()
            if mietverhaeltnis.vertragsbeginn > today:
                return redirect('kostenpruefung_mietobjekte_app:mieter_zukuenftig')
            elif mietverhaeltnis.vertragsende < today:
                return redirect('kostenpruefung_mietobjekte_app:mieter_archiv')
            else:
                return redirect('kostenpruefung_mietobjekte_app:mieter_laufend')
    else:
        # Initial form display or after selecting Mietobjekt
        form = MietverhaeltnisForm(initial=initial_data, user=request.user)
    
    return render(request, 'kostenpruefung_mietobjekte_app/mietverhaeltnis_form.html', {
        'form': form,
        'mieter': mieter,
        'selected_mietobjekt': selected_mietobjekt
    })


# ═══════════════════════════════════════════════════════════════════════════════
# ██████████████████ CLASS-BASED VIEWS (UPDATE/DELETE) █████████████████████████
# ═══════════════════════════════════════════════════════════════════════════════

# ─────────────────────────── MIETOBJEKT UPDATE/DELETE ────────────────────────

class MietobjektUpdateView(LoginRequiredMixin, UpdateView):
    model = Mietobjekt
    form_class = MietobjektForm
    template_name = 'kostenpruefung_mietobjekte_app/mietobjekt_form.html'

    def get_queryset(self):
        # Only allow editing objects created by the user
        return Mietobjekt.objects.filter(created_by=self.request.user)

    def get_success_url(self):
        return reverse_lazy('kostenpruefung_mietobjekte_app:objekt_index')

class MietobjektDeleteView(LoginRequiredMixin, DeleteView):
    model = Mietobjekt
    template_name = 'kostenpruefung_mietobjekte_app/mietobjekt_confirm_delete.html'

    def get_queryset(self):
        # Only allow deleting objects created by the user
        return Mietobjekt.objects.filter(created_by=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['password_form'] = PasswordConfirmationForm()
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = PasswordConfirmationForm(request.POST)
        
        if form.is_valid():
            # Check if password is correct
            password = form.cleaned_data['password']
            user = request.user
            
            if user.check_password(password):
                # Password is correct, proceed with deletion
                self.object.delete()
                return HttpResponseRedirect(self.get_success_url())
            else:
                # Password is incorrect
                form.add_error('password', 'Das Passwort ist nicht korrekt.')
        
        # If form is invalid or password is incorrect, redisplay the form
        return self.render_to_response(
            self.get_context_data(object=self.object, password_form=form)
        )

    def get_success_url(self):
        return reverse_lazy('kostenpruefung_mietobjekte_app:objekt_index')


# ─────────────────────────── MIETER UPDATE/DELETE ────────────────────────────

class MieterUpdateView(LoginRequiredMixin, UpdateView):
    model = Mieter
    form_class = MieterObjektForm
    template_name = 'kostenpruefung_mietobjekte_app/mieter_form.html'

    def get_queryset(self):
        return Mieter.objects.filter(created_by=self.request.user)

    def get_success_url(self):
        return reverse_lazy('kostenpruefung_mietobjekte_app:mieter_laufend')

class MieterDeleteView(LoginRequiredMixin, DeleteView):
    model = Mieter
    template_name = 'kostenpruefung_mietobjekte_app/mieter_confirm_delete.html'

    def get_queryset(self):
        return Mieter.objects.filter(created_by=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['password_form'] = PasswordConfirmationForm()
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = PasswordConfirmationForm(request.POST)
        
        if form.is_valid():
            password = form.cleaned_data['password']
            user = request.user
            
            if user.check_password(password):
                self.object.delete()
                return HttpResponseRedirect(self.get_success_url())
            else:
                form.add_error('password', 'Das Passwort ist nicht korrekt.')
        
        return self.render_to_response(
            self.get_context_data(object=self.object, password_form=form)
        )

    def get_success_url(self):
        return reverse_lazy('kostenpruefung_mietobjekte_app:mieter_laufend')


# ─────────────────────────── RECHNUNG UPDATE/DELETE ───────────────────────────

class RechnungUpdateView(LoginRequiredMixin, UpdateView):
    model = Rechnung
    form_class = RechnungForm
    template_name = 'kostenpruefung_mietobjekte_app/rechnung_form.html'

    def get_queryset(self):
        return Rechnung.objects.filter(created_by=self.request.user)

    def get_success_url(self):
        return reverse_lazy('kostenpruefung_mietobjekte_app:rechnungen')

class RechnungDeleteView(LoginRequiredMixin, DeleteView):
    model = Rechnung
    template_name = 'kostenpruefung_mietobjekte_app/rechnung_confirm_delete.html'

    def get_queryset(self):
        return Rechnung.objects.filter(created_by=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['password_form'] = PasswordConfirmationForm()
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = PasswordConfirmationForm(request.POST)
        
        if form.is_valid():
            password = form.cleaned_data['password']
            user = request.user
            
            if user.check_password(password):
                self.object.delete()
                return HttpResponseRedirect(self.get_success_url())
            else:
                form.add_error('password', 'Das Passwort ist nicht korrekt.')
        
        return self.render_to_response(
            self.get_context_data(object=self.object, password_form=form)
        )

    def get_success_url(self):
        return reverse_lazy('kostenpruefung_mietobjekte_app:rechnungen')


# ─────────────────────────── RECHNUNGSART (Kostenarten) UPDATE/DELETE ───────────────────────

class RechnungsartUpdateView(LoginRequiredMixin, UpdateView):
    model = Rechnungsart
    form_class = RechnungsartForm
    template_name = 'kostenpruefung_mietobjekte_app/rechnungsart_form.html'

    def get_queryset(self):
        return Rechnungsart.objects.filter(created_by=self.request.user)

    def get_success_url(self):
        return reverse_lazy('kostenpruefung_mietobjekte_app:kostenarten')

class RechnungsartDeleteView(LoginRequiredMixin, DeleteView):
    model = Rechnungsart
    template_name = 'kostenpruefung_mietobjekte_app/rechnungsart_confirm_delete.html'

    def get_queryset(self):
        return Rechnungsart.objects.filter(created_by=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['password_form'] = PasswordConfirmationForm()
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = PasswordConfirmationForm(request.POST)
        
        if form.is_valid():
            password = form.cleaned_data['password']
            user = request.user
            
            if user.check_password(password):
                self.object.delete()
                return HttpResponseRedirect(self.get_success_url())
            else:
                form.add_error('password', 'Das Passwort ist nicht korrekt.')
        
        return self.render_to_response(
            self.get_context_data(object=self.object, password_form=form)
        )

    def get_success_url(self):
        return reverse_lazy('kostenpruefung_mietobjekte_app:kostenarten')


# ─────────────────────────── LIEFERANT UPDATE/DELETE ──────────────────────────

class LieferantUpdateView(LoginRequiredMixin, UpdateView):
    model = Lieferant
    form_class = LieferantForm
    template_name = 'kostenpruefung_mietobjekte_app/lieferant_form.html'

    def get_queryset(self):
        return Lieferant.objects.filter(created_by=self.request.user)

    def get_success_url(self):
        return reverse_lazy('kostenpruefung_mietobjekte_app:lieferanten')

class LieferantDeleteView(LoginRequiredMixin, DeleteView):
    model = Lieferant
    template_name = 'kostenpruefung_mietobjekte_app/lieferant_confirm_delete.html'

    def get_queryset(self):
        return Lieferant.objects.filter(created_by=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['password_form'] = PasswordConfirmationForm()
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = PasswordConfirmationForm(request.POST)
        
        if form.is_valid():
            password = form.cleaned_data['password']
            user = request.user
            
            if user.check_password(password):
                self.object.delete()
                return HttpResponseRedirect(self.get_success_url())
            else:
                form.add_error('password', 'Das Passwort ist nicht korrekt.')
        
        return self.render_to_response(
            self.get_context_data(object=self.object, password_form=form)
        )

    def get_success_url(self):
        return reverse_lazy('kostenpruefung_mietobjekte_app:lieferanten')


# ─────────────────────────── KONTO UPDATE/DELETE ──────────────────────────────

class KontoUpdateView(LoginRequiredMixin, UpdateView):
    model = Konto
    form_class = KontoForm
    template_name = 'kostenpruefung_mietobjekte_app/konto_form.html'

    def get_queryset(self):
        return Konto.objects.filter(created_by=self.request.user)

    def get_success_url(self):
        return reverse_lazy('kostenpruefung_mietobjekte_app:konto')

class KontoDeleteView(LoginRequiredMixin, DeleteView):
    model = Konto
    template_name = 'kostenpruefung_mietobjekte_app/konto_confirm_delete.html'

    def get_queryset(self):
        return Konto.objects.filter(created_by=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['password_form'] = PasswordConfirmationForm()
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = PasswordConfirmationForm(request.POST)
        
        if form.is_valid():
            password = form.cleaned_data['password']
            user = request.user
            
            if user.check_password(password):
                self.object.delete()
                return HttpResponseRedirect(self.get_success_url())
            else:
                form.add_error('password', 'Das Passwort ist nicht korrekt.')
        
        return self.render_to_response(
            self.get_context_data(object=self.object, password_form=form)
        )

    def get_success_url(self):
        return reverse_lazy('kostenpruefung_mietobjekte_app:konto')