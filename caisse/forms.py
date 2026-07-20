from django import forms
from services.models import ServiceMedical


class EmissionTicketForm(forms.Form):
    service = forms.ModelChoiceField(
        queryset=ServiceMedical.objects.filter(actif=True),
        label="Service médical",
        empty_label="-- Choisir un service --",
    )
