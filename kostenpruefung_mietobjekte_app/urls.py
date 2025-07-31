# ═══════════════════════════════════════════════════════════════════════════════
# █████████████████████████████ URL IMPORTS ███████████████████████████████████
# ═══════════════════════════════════════════════════════════════════════════════

from django.urls import path

# Function-based views imports
from .views import (objekt_index, mieter, rechnungen, kostenarten, lieferanten, konto, auswertung, 
                    mieter_laufend, mieter_zukuenftig, mieter_archiv)
from .views import mietobjekt_create, rechnung_create, rechnungsart_create, lieferant_create, konto_create
from .views import mieteinheit_create, prozent_bulk_update, mieter_create_step1, mietverhaeltnis_create

# Class-based views imports
from .views import MietobjektUpdateView, MietobjektDeleteView
from .views import (MieterUpdateView, MieterDeleteView, 
                   RechnungUpdateView, RechnungDeleteView,
                   RechnungsartUpdateView, RechnungsartDeleteView,
                   LieferantUpdateView, LieferantDeleteView,
                   KontoUpdateView, KontoDeleteView)


# ═══════════════════════════════════════════════════════════════════════════════
# █████████████████████████████ URL PATTERNS ██████████████████████████████████
# ═══════════════════════════════════════════════════════════════════════════════
app_name = 'kostenpruefung_mietobjekte_app'
urlpatterns = [

    # ─────────────────────────── MAIN INDEX ──────────────────────────────
    path('', objekt_index, name='objekt_index'),

    # ─────────────────────────── MIETOBJEKT URLS ─────────────────────────
    path('mietobjekt/create/', mietobjekt_create, name='mietobjekt_create'),
    path('mietobjekt/<int:pk>/update/', MietobjektUpdateView.as_view(), name='mietobjekt_update'),
    path('mietobjekt/<int:pk>/delete/', MietobjektDeleteView.as_view(), name='mietobjekt_delete'),
    
    # ─────────────────────────── MIETEINHEIT URLS ────────────────────────
    path('mieteinheit/create/<int:mietobjekt_id>/', mieteinheit_create, name='mieteinheit_create'),
    
    # ─────────────────────────── MIETER URLS ─────────────────────────────
    path('mieter/', mieter, name='mieter'),
    path('mieter/laufend/', mieter_laufend, name='mieter_laufend'),
    path('mieter/zukuenftig/', mieter_zukuenftig, name='mieter_zukuenftig'),
    path('mieter/archiv/', mieter_archiv, name='mieter_archiv'),
    path('mieter/create/step1/', mieter_create_step1, name='mieter_create_step1'),
    path('mieter/<int:pk>/update/', MieterUpdateView.as_view(), name='mieter_update'),
    path('mieter/<int:pk>/delete/', MieterDeleteView.as_view(), name='mieter_delete'),
    
    # ─────────────────────────── MIETVERHAELTNIS URLS ────────────────────
    path('mieter/<int:mieter_id>/mietverhaeltnis/create/', mietverhaeltnis_create, name='mietverhaeltnis_create'),
    
    # ─────────────────────────── RECHNUNG URLS ───────────────────────────
    path('rechnungen/', rechnungen, name='rechnungen'),
    path('rechnung/create/', rechnung_create, name='rechnung_create'),
    path('rechnung/<int:pk>/update/', RechnungUpdateView.as_view(), name='rechnung_update'),
    path('rechnung/<int:pk>/delete/', RechnungDeleteView.as_view(), name='rechnung_delete'),
    
    # ─────────────────────────── PROZENT URLS ────────────────────────────
    path('prozent/bulk_update/<int:rechnung_id>/', prozent_bulk_update, name='prozent_bulk_update'),
    
    # ─────────────────────────── RECHNUNGSART/KOSTENARTEN URLS ───────────
    path('kostenarten/', kostenarten, name='kostenarten'),
    path('rechnungsart/create/', rechnungsart_create, name='rechnungsart_create'),
    path('rechnungsart/<int:pk>/update/', RechnungsartUpdateView.as_view(), name='rechnungsart_update'),
    path('rechnungsart/<int:pk>/delete/', RechnungsartDeleteView.as_view(), name='rechnungsart_delete'),
    
    # ─────────────────────────── LIEFERANT URLS ──────────────────────────
    path('lieferanten/', lieferanten, name='lieferanten'),
    path('lieferant/create/', lieferant_create, name='lieferant_create'),
    path('lieferant/<int:pk>/update/', LieferantUpdateView.as_view(), name='lieferant_update'),
    path('lieferant/<int:pk>/delete/', LieferantDeleteView.as_view(), name='lieferant_delete'),
    
    # ─────────────────────────── KONTO URLS ──────────────────────────────
    path('konto/', konto, name='konto'),
    path('konto/create/', konto_create, name='konto_create'),
    path('konto/<int:pk>/update/', KontoUpdateView.as_view(), name='konto_update'),
    path('konto/<int:pk>/delete/', KontoDeleteView.as_view(), name='konto_delete'),
    
    # ─────────────────────────── AUSWERTUNG URLS ─────────────────────────
    path('auswertung/', auswertung, name='auswertung'),

]