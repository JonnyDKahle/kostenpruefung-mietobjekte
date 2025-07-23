from django.db import models
import datetime


class Mietobjekt(models.Model):
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
    vorname = models.CharField(max_length=255)
    nachname = models.CharField(max_length=255)
    strasse_hausnummer = models.CharField(max_length=255)
    plz = models.IntegerField()
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

    mietobjekte = models.ManyToManyField(Mietobjekt)

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