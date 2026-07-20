from django import forms

INPUT_CLASS = "w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-clinique-bleu placeholder:text-gray-300"


class RecherchePatientForm(forms.Form):
    telephone = forms.CharField(required=False, label="Téléphone", widget=forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': '77 123 45 67'}))
    numero_patient = forms.CharField(required=False, label="Numéro de carte patient", widget=forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': 'PAT-...'}))
    nom = forms.CharField(required=False, label="Nom", widget=forms.TextInput(attrs={'class': INPUT_CLASS}))
    prenom = forms.CharField(required=False, label="Prénom", widget=forms.TextInput(attrs={'class': INPUT_CLASS}))
    date_naissance = forms.DateField(required=False, label="Date de naissance", widget=forms.DateInput(attrs={'type': 'date', 'class': INPUT_CLASS}))


class CreationPatientForm(forms.ModelForm):
    class Meta:
        from .models import Patient
        model = Patient
        fields = ['nom', 'prenom', 'telephone', 'date_naissance', 'categorie', 'quartier_village']
        widgets = {
            'nom': forms.TextInput(attrs={'class': INPUT_CLASS}),
            'prenom': forms.TextInput(attrs={'class': INPUT_CLASS}),
            'telephone': forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Optionnel'}),
            'date_naissance': forms.DateInput(attrs={'type': 'date', 'class': INPUT_CLASS}),
            'categorie': forms.Select(attrs={'class': INPUT_CLASS}),
            'quartier_village': forms.Select(attrs={'class': INPUT_CLASS}),
        }
