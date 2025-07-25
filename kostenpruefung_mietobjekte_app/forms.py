from django import forms
from .models import Mietobjekt

class MietobjektForm(forms.ModelForm):
    kaufdatum = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Mietobjekt
        exclude = ['created_by']
        widgets = {
            'kaufdatum': forms.DateInput(attrs={'type': 'date'}),
        }