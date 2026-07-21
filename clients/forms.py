from django import forms
from .models import Client

INPUT_CLASS = "w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-clinique-bleu"


class OnboardingCliniqueForm(forms.Form):
    nom_clinique = forms.CharField(label="Nom de la clinique", widget=forms.TextInput(attrs={'class': INPUT_CLASS}))
    schema_name = forms.SlugField(
        label="Identifiant technique (sans espace, minuscules, ex: clinique-liberte)",
        widget=forms.TextInput(attrs={'class': INPUT_CLASS}),
    )
    sous_domaine = forms.SlugField(
        label="Sous-domaine (ex: clinique-liberte)",
        widget=forms.TextInput(attrs={'class': INPUT_CLASS}),
    )
    plan_abonnement = forms.ChoiceField(
        label="Formule",
        choices=[('essai', 'Essai gratuit'), ('standard', 'Standard'), ('premium', 'Premium')],
        widget=forms.Select(attrs={'class': INPUT_CLASS}),
    )
    admin_prenom = forms.CharField(label="Prénom de l'Admin Clinique", widget=forms.TextInput(attrs={'class': INPUT_CLASS}))
    admin_nom = forms.CharField(label="Nom de l'Admin Clinique", widget=forms.TextInput(attrs={'class': INPUT_CLASS}))
    admin_username = forms.CharField(label="Identifiant de connexion", widget=forms.TextInput(attrs={'class': INPUT_CLASS}))
    admin_password = forms.CharField(label="Mot de passe initial", widget=forms.PasswordInput(attrs={'class': INPUT_CLASS}))

    def clean_schema_name(self):
        schema_name = self.cleaned_data['schema_name'].replace('-', '_')
        if Client.objects.filter(schema_name=schema_name).exists():
            raise forms.ValidationError("Cet identifiant technique est déjà utilisé.")
        return schema_name
