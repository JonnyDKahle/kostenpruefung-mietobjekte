from django.db import models
import datetime
from django.contrib.auth import get_user_model
User = get_user_model()


class Mietobjekt(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="mietobjekte_created", null=True, blank=True)
    name = models.CharField(max_length=255)
    strasse_hausnummer = models.CharField(max_length=255)
    plz = models.IntegerField()
    ort = models.CharField(max_length=100)
    land = models.CharField(max_length=100)

    kaufdatum = models.DateField()
    kaufpreis = models.DecimalField()
    darlehen = models.DecimalField()
    grundschuld = models.DecimalField()
    FARBE_CHOICES = [
        ('rot', 'Rot'),
        ('blau', 'Blau'),
        ('gruen', 'Grün'),
        ('gelb', 'Gelb'),
        ('schwarz', 'Schwarz'),
    ]
    farbe = models.CharField(max_length=20, choices=FARBE_CHOICES)

    def __str__(self):
        return self.name

class Mieter(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="mieter_created", null=True, blank=True)
    vorname = models.CharField(max_length=255)
    nachname = models.CharField(max_length=255)
    strasse_hausnummer = models.CharField(max_length=255)
    plz = models.CharField()
    ort = models.CharField(max_length=100)
    land = models.CharField(max_length=100)
    telefon = models.CharField(max_length=100)
    e_mail = models.EmailField()
    geburtsdatum = models.DateField()

    vertragsbeginn = models.DateField()
    vertragsende = models.DateField()

    kaltmiete = models.DecimalField()
    nebenkosten = models.DecimalField()
    kaution = models.DecimalField()

    mietobjekte = models.ManyToManyField('Mietobjekt')

    @property
    def mietstatus(self):
        today = datetime.date.today()
        if self.vertragsbeginn > today:
            return "future"
        elif self.vertragsende < today:
            return "past"
        else:
            return "current"
        
    def __str__(self):
        return f"{self.vorname} {self.nachname}"
    

class Rechnung(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rechnungen_created", null=True, blank=True)
    datum = models.DateField()
    rechnungsnummer = models.CharField(max_length=255)
    name = models.CharField(max_length=255) # Descriptive name to identify the payment
    betrag = models.DecimalField()
    art = models.ForeignKey('Rechnungsart', on_delete=models.PROTECT)
    lieferant = models.ManyToManyField('Lieferant')
    bezahlt_am = models.DateField()
    #offener_betrag = ... # What is the idea here? Should there be a place where costs that where the due date is now are listed? Where do they come from?
    #konto = ... # Add model first
    mietobjekte = models.ManyToManyField('Mietobjekt') # What is the idea of the Percentage? Is the idea all the apartments of a tenant are listed? Confusing?
    #Anteil = ... # This is somehow conneted to the column above. Only if the percentage of the above column sums up to 100, the "Rechnung" can be created.

    def __str__(self):
        return f"Rechnung {self.rechnungsnummer} - {self.name}"
    
class Rechnungsart(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rechnungsarten_created", null=True, blank=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class Lieferant(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lieferanten_created", null=True, blank=True)
    firmenname = models.CharField(max_length=255)
    vorname = models.CharField(max_length=255)
    nachname = models.CharField(max_length=255)
    strasse = models.CharField(max_length=255)
    hausnummer = models.CharField(max_length=10)
    plz = models.CharField(max_length=10) # 2 - 10 characters (numbers and letters)
    ort = models.CharField(max_length=100)
    land = models.CharField(max_length=100)
    e_mail = models.EmailField()
    telefon = models.CharField(max_length=100)

# class Konto(models.Model):
#     buchungstag = models.DateField()
#     kontoinhaber = models.CharField(max_length=255) # 
#     buchungstext =      # (Aus Kontoauszug)
#     wertstellung =      # (Datum)
#     buchungsart =       # (Lastschrift - z.B. Ueberweisung)
#     mieter = models.ManyToManyField('Mieter')
#     lieferanten = models.ManyToManyField('Lieferant')
