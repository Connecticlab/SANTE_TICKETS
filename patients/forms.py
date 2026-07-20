from django import forms


class RecherchePatientForm(forms.Form):
    telephone = forms.CharField(required=False, label="Téléphone")
    numero_patient = forms.CharField(required=False, label="Numéro de carte patient")
    nom = forms.CharField(required=False, label="Nom")
    prenom = forms.CharField(required=False, label="Prénom")
    date_naissance = forms.DateField(required=False, label="Date de naissance", widget=forms.DateInput(attrs={'type': 'date'}))


class CreationPatientForm(forms.ModelForm):
    class Meta:
        from .models import Patient
        model = Patient
        fields = ['nom', 'prenom', 'telephone', 'date_naissance', 'categorie', 'quartier_village']
        widgets = {
            'date_naissance': forms.DateInput(attrs={'type': 'date'}),
        }
