from django.db import models

class Mietobjekt(models.Model):
    name = models.CharField(max_length=255)
    strasse_hausnummer = models.CharField(max_length=255)
    plz = models.IntegerField()
    ort = models.CharField(max_length=100)
    land = models.CharField(max_length=100)
    kaufdatum = models.DateField()
    kaufpreis = models.FloatField()
    darlehen = models.FloatField()
    grundschuld = models.FloatField()
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
