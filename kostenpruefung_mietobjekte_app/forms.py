from django import forms
from .models import Mietobjekt, Rechnung, Rechnungsart, Lieferant, Konto, Mieteinheit, Prozent

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
        fields = ['prozent']  # Only show the percentage field
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