from django import forms
from django.contrib.auth.models import User

INPUT_CLASS = "w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-clinique-bleu"


class CreationCompteForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", widget=forms.TextInput(attrs={'class': INPUT_CLASS}))
    nom = forms.CharField(label="Nom", widget=forms.TextInput(attrs={'class': INPUT_CLASS}))
    prenom = forms.CharField(label="Prénom", widget=forms.TextInput(attrs={'class': INPUT_CLASS}))
    telephone = forms.CharField(label="Téléphone", required=False, widget=forms.TextInput(attrs={'class': INPUT_CLASS}))
    role = forms.ChoiceField(
        label="Rôle",
        choices=[('caissier', 'Caissier'), ('admin_clinique', 'Admin Clinique')],
        widget=forms.Select(attrs={'class': INPUT_CLASS}),
    )
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput(attrs={'class': INPUT_CLASS}))

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Ce nom d'utilisateur est déjà pris.")
        return username


class ModifierCompteForm(forms.Form):
    nom = forms.CharField(label="Nom", widget=forms.TextInput(attrs={'class': INPUT_CLASS}))
    prenom = forms.CharField(label="Prénom", widget=forms.TextInput(attrs={'class': INPUT_CLASS}))
    telephone = forms.CharField(label="Téléphone", required=False, widget=forms.TextInput(attrs={'class': INPUT_CLASS}))
    role = forms.ChoiceField(
        label="Rôle",
        choices=[('caissier', 'Caissier'), ('admin_clinique', 'Admin Clinique')],
        widget=forms.Select(attrs={'class': INPUT_CLASS}),
    )
    nouveau_mot_de_passe = forms.CharField(
        label="Nouveau mot de passe (laisser vide pour ne pas changer)",
        required=False,
        widget=forms.PasswordInput(attrs={'class': INPUT_CLASS}),
    )
