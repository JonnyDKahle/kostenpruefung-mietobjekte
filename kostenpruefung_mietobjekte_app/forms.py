from django import forms
from .models import Mietobjekt, Rechnung, Rechnungsart, Lieferant

class MietobjektForm(forms.ModelForm):
    kaufdatum = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Mietobjekt
        exclude = ['created_by']
        widgets = {
            'kaufdatum': forms.DateInput(attrs={'type': 'date'}),
        }

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
    
class RechnungsartForm(forms.ModelForm):
    class Meta:
        model = Rechnungsart
        exclude = ['created_by']

class LieferantForm(forms.ModelForm):

    class Meta:
        model = Lieferant
        exclude = ['created_by']
