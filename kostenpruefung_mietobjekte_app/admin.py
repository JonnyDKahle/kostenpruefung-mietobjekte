from django.contrib import admin
from .models import Mietobjekt, Mieter, Rechnung, Rechnungsart, Lieferant, Prozent, Mieteinheit, Konto

admin.site.register(Mietobjekt)
admin.site.register(Mieter)
admin.site.register(Rechnung)
admin.site.register(Rechnungsart)
admin.site.register(Lieferant)
admin.site.register(Prozent)
admin.site.register(Mieteinheit)
admin.site.register(Konto)