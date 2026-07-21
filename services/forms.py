from django import forms
from .models import ServiceMedical, TarifService

INPUT_CLASS = "w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-clinique-bleu"


class ServiceMedicalForm(forms.ModelForm):
    class Meta:
        model = ServiceMedical
        fields = ['nom', 'code', 'description', 'actif']
        widgets = {
            'nom': forms.TextInput(attrs={'class': INPUT_CLASS}),
            'code': forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': 'ex: CONSULT-GEN'}),
            'description': forms.Textarea(attrs={'class': INPUT_CLASS, 'rows': 3}),
        }


class TarifServiceForm(forms.ModelForm):
    class Meta:
        model = TarifService
        fields = ['categorie_patient', 'montant', 'gratuit', 'date_effet']
        widgets = {
            'categorie_patient': forms.Select(attrs={'class': INPUT_CLASS}),
            'montant': forms.NumberInput(attrs={'class': INPUT_CLASS}),
            'date_effet': forms.DateInput(attrs={'type': 'date', 'class': INPUT_CLASS}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from patients.models import CategoriePatient
        choix_categories = [(c.code, c.libelle) for c in CategoriePatient.objects.filter(actif=True)]
        if choix_categories:
            self.fields['categorie_patient'].widget = forms.Select(
                choices=choix_categories,
                attrs={'class': INPUT_CLASS},
            )
