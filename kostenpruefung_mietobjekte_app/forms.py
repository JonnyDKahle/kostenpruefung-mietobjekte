from django import forms
from .models import Mietobjekt, Rechnung, Rechnungsart, Lieferant, Konto, Mieteinheit, Prozent, Mieter, Mietverhaeltnis

class MietobjektForm(forms.ModelForm):
    kaufdatum = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Mietobjekt
        exclude = ['created_by']
        widgets = {
            'kaufdatum': forms.DateInput(attrs={'type': 'date'}),
        }

class MieteinheitForm(forms.ModelForm):
    class Meta:
        model = Mieteinheit
        fields = ['name']

#### Mieter Here!! 

class MieterObjektForm(forms.ModelForm):
    class Meta:
        model = Mieter
        fields = ['vorname', 'nachname', 'telefon', 'e_mail', 'geburtsdatum']
        widgets = {
            'geburtsdatum': forms.DateInput(attrs={'type': 'date'}),
        }

class RechnungForm(forms.ModelForm):
    datum = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    bezahlt_am = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Rechnung
        exclude = ['created_by']
        widgets = {
            'datum': forms.DateInput(attrs={'type': 'date'}),
            'bezahlt_am': forms.DateInput(attrs={'type': 'date'}),
        }

class ProzentForm(forms.ModelForm):
    class Meta:
        model = Prozent
        # fields = ['prozent']  # Only show the percentage field
        fields = '__all__'
        widgets = {
            'prozent': forms.NumberInput(attrs={'step': '0.01'}),
        }
    
class RechnungsartForm(forms.ModelForm):
    class Meta:
        model = Rechnungsart
        exclude = ['created_by']

class LieferantForm(forms.ModelForm):

    class Meta:
        model = Lieferant
        exclude = ['created_by']

class KontoForm(forms.ModelForm):
    buchungstag = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    werterstellung = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Konto
        exclude = ['created_by']
        widgets = {
            'buchungstag': forms.DateInput(attrs={'type': 'date'}),
            'werterstellung': forms.DateInput(attrs={'type': 'date'}),
        }

class MietverhaeltnisForm(forms.ModelForm):
    class Meta:
        model = Mietverhaeltnis
        fields = ['strasse_hausnummer', 'plz', 'ort', 'land', 
                  'vertragsbeginn', 'vertragsende', 'kaltmiete', 
                  'nebenkosten', 'kaution', 'mietobjekte', 'mieteinheiten']
        widgets = {
            'vertragsbeginn': forms.DateInput(attrs={'type': 'date'}),
            'vertragsende': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # If you want to filter mieteinheiten based on selected mietobjekte,
        # you could add custom JS or modify the form's clean method