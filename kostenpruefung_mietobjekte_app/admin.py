from django.contrib import admin
from .models import (
    Mietobjekt, Mieteinheit, Mieter, Mietverhaeltnis, Rechnung, Rechnungsart,
    Lieferant, Prozent, Konto, Buchungsart
)

admin.site.register(Mietobjekt)
admin.site.register(Mieteinheit)
admin.site.register(Mieter)
admin.site.register(Mietverhaeltnis)
admin.site.register(Rechnung)
admin.site.register(Rechnungsart)
admin.site.register(Lieferant)
admin.site.register(Prozent)
admin.site.register(Konto)
admin.site.register(Buchungsart)