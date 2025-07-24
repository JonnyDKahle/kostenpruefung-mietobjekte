from django.contrib import admin
from .models import Mietobjekt, Mieter, Rechnung, Rechnungsart, Lieferant

admin.site.register(Mietobjekt)
admin.site.register(Mieter)
admin.site.register(Rechnung)
admin.site.register(Rechnungsart)
admin.site.register(Lieferant)
