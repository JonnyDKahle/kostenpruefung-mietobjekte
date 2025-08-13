from django import forms
from .models import Mietobjekt, Rechnung, Rechnungsart, Lieferant, Konto, Mieteinheit, Prozent, Mieter, Mietverhaeltnis

class MietobjektForm(forms.ModelForm):
    class Meta:
        model = Mietobjekt
        exclude = ['created_by']

class MieteinheitForm(forms.ModelForm):
    class Meta:
        model = Mieteinheit
        fields = ['name', 'kaufdatum', 'kaufpreis', 'darlehen', 'grundschuld']
        widgets = {
            'kaufdatum': forms.DateInput(attrs={'type': 'date'}),
        }

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
        fields = ['name', 'farbe']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'farbe': forms.TextInput(attrs={
                'type': 'color',
                'class': 'form-control color-picker',
                'title': 'Wählen Sie eine Farbe für diese Kostenart'
            })
        }
        labels = {
            'name': 'Name der Kostenart',
            'farbe': 'Farbe für Diagramme'
        }

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
    # Single field for selecting one Mietobjekt
    mietobjekt = forms.ModelChoiceField(
        queryset=Mietobjekt.objects.all(),
        label="Mietobjekt",
        required=True
    )
    
    class Meta:
        model = Mietverhaeltnis
        fields = ['mietobjekt', 'mieteinheiten', 'vertragsbeginn', 
                  'vertragsende', 'kaltmiete', 'nebenkosten', 'kaution',
                  'strasse_hausnummer', 'plz', 'ort', 'land']
        widgets = {
            'vertragsbeginn': forms.DateInput(attrs={'type': 'date'}),
            'vertragsende': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['mietobjekt'].queryset = Mietobjekt.objects.filter(created_by=user)
            # Show all mieteinheiten initially - JavaScript will filter them
            self.fields['mieteinheiten'].queryset = Mieteinheit.objects.filter(mietobjekt__created_by=user)
            
            # If we have a selected mietobjekt in GET/POST data, filter the mieteinheiten
            if 'mietobjekt' in self.data:
                try:
                    mietobjekt_id = int(self.data.get('mietobjekt'))
                    self.fields['mieteinheiten'].queryset = Mieteinheit.objects.filter(mietobjekt_id=mietobjekt_id)
                except (ValueError, TypeError):
                    pass
            elif self.instance.pk and hasattr(self.instance, 'mietobjekte'):
                # For editing existing instances, show mieteinheiten of the first mietobjekt
                if self.instance.mietobjekte.exists():
                    first_mietobjekt = self.instance.mietobjekte.first()
                    self.fields['mieteinheiten'].queryset = first_mietobjekt.mieteinheiten.all()
        
class PasswordConfirmationForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}), 
        label="Passwort zur Bestätigung",
        help_text="Bitte geben Sie Ihr Passwort ein, um die Löschung zu bestätigen."
    )