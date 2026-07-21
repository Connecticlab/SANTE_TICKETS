from django import forms
from services.models import ServiceMedical


class EmissionTicketForm(forms.Form):
    service = forms.ModelChoiceField(
        queryset=ServiceMedical.objects.filter(actif=True),
        label="Service médical",
        empty_label="-- Choisir un service --",
    )


class ModificationTicketForm(forms.ModelForm):
    class Meta:
        from .models import Ticket
        model = Ticket
        fields = ['service', 'montant', 'statut_paiement']
        widgets = {
            'service': forms.Select(attrs={'class': 'w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-clinique-bleu'}),
            'montant': forms.NumberInput(attrs={'class': 'w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-clinique-bleu'}),
            'statut_paiement': forms.Select(attrs={'class': 'w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-clinique-bleu'}),
        }
