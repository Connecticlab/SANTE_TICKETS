from django import forms
from .models import Localite

INPUT_CLASS = "w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-clinique-bleu"


class LocaliteForm(forms.ModelForm):
    class Meta:
        model = Localite
        fields = ['nom', 'commune', 'actif']
        widgets = {
            'nom': forms.TextInput(attrs={'class': INPUT_CLASS}),
            'commune': forms.Select(attrs={'class': INPUT_CLASS}),
        }
