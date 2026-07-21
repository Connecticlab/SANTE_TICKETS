from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import RecherchePatientForm, CreationPatientForm
from .services import rechercher_patient


@login_required
def rechercher_patient_view(request):
    resultat = None
    methode = None
    recherche_effectuee = False

    if request.method == 'POST':
        form = RecherchePatientForm(request.POST)
        if form.is_valid():
            recherche_effectuee = True
            resultat, methode = rechercher_patient(
                telephone=form.cleaned_data.get('telephone') or None,
                numero_patient=form.cleaned_data.get('numero_patient') or None,
                nom=form.cleaned_data.get('nom') or None,
                prenom=form.cleaned_data.get('prenom') or None,
                date_naissance=form.cleaned_data.get('date_naissance') or None,
            )
    else:
        form = RecherchePatientForm()

    context = {
        'form': form,
        'resultat': resultat,
        'methode': methode,
        'recherche_effectuee': recherche_effectuee,
    }
    return render(request, 'patients/rechercher.html', context)


@login_required
def creer_patient_view(request):
    if request.method == 'POST':
        form = CreationPatientForm(request.POST)
        if form.is_valid():
            patient = form.save()
            return redirect('nouveau_ticket', patient_id=patient.id)
    else:
        form = CreationPatientForm()

    return render(request, 'patients/creer.html', {'form': form})


import qrcode
from io import BytesIO
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required as _login_required


@_login_required
def qr_code_patient(request, patient_id):
    from .models import Patient
    from django.urls import reverse
    patient = Patient.objects.get(id=patient_id)
    url_scan = request.build_absolute_uri(reverse('scanner_patient')) + f"?qr={patient.qr_code}"
    img = qrcode.make(url_scan)
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    return HttpResponse(buffer.getvalue(), content_type='image/png')


def scanner_patient(request):
    from .models import Patient
    from django.shortcuts import redirect as _redirect
    qr = request.GET.get('qr')
    if qr:
        patient = Patient.objects.filter(qr_code=qr).first()
        if patient and request.user.is_authenticated:
            return _redirect('nouveau_ticket', patient_id=patient.id)
    return render(request, 'patients/scan_patient.html', {'trouve': False, 'qr': qr})


@_login_required
def liste_patients_view(request):
    from .models import Patient
    patients = Patient.objects.all().order_by('-date_creation')

    recherche = request.GET.get('q')
    if recherche:
        patients = patients.filter(
            nom__icontains=recherche
        ) | patients.filter(
            prenom__icontains=recherche
        ) | patients.filter(
            telephone__icontains=recherche
        )

    patients = patients[:50]
    return render(request, 'patients/liste.html', {'patients': patients, 'recherche': recherche or ''})


@_login_required
def detail_patient_view(request, patient_id):
    from .models import Patient
    from .forms import CreationPatientForm
    patient = Patient.objects.get(id=patient_id)

    if request.method == 'POST':
        form = CreationPatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            from audit.models import enregistrer_action
            enregistrer_action(
                utilisateur=request.user,
                action='modification',
                modele_cible='Patient',
                objet_id=patient.numero_patient,
                details="Informations patient modifiees",
            )
            return redirect('liste_patients')
    else:
        form = CreationPatientForm(instance=patient)

    profile = getattr(request.user, 'profile', None)
    peut_supprimer = profile and profile.est_admin_clinique()

    return render(request, 'patients/detail.html', {
        'patient': patient,
        'form': form,
        'peut_supprimer': peut_supprimer,
    })


@_login_required
def supprimer_patient_view(request, patient_id):
    from .models import Patient
    from django.contrib.auth.decorators import login_required
    patient = Patient.objects.get(id=patient_id)

    profile = getattr(request.user, 'profile', None)
    if not (profile and profile.est_admin_clinique()):
        return redirect('detail_patient', patient_id=patient.id)

    erreur = None
    if request.method == 'POST':
        from django.db.models import ProtectedError
        from audit.models import enregistrer_action
        numero = patient.numero_patient
        try:
            patient.delete()
            enregistrer_action(
                utilisateur=request.user,
                action='annulation',
                modele_cible='Patient',
                objet_id=numero,
                details=f"Suppression du patient {patient.prenom} {patient.nom}",
            )
            return redirect('liste_patients')
        except ProtectedError:
            erreur = "Ce patient a des tickets associes et ne peut pas etre supprime. L'historique doit etre conserve."

    return render(request, 'patients/confirmer_suppression.html', {'patient': patient, 'erreur': erreur})


from comptes.decorators import admin_clinique_required
from django.contrib import messages as django_messages
from django.db.models import ProtectedError


@admin_clinique_required
def liste_categories(request):
    from .models import CategoriePatient
    categories = CategoriePatient.objects.all().order_by('libelle')
    return render(request, 'patients/categories_liste.html', {'categories': categories})


@admin_clinique_required
def creer_categorie(request):
    from .models import CategoriePatient
    from django import forms as django_forms

    class CategorieForm(django_forms.ModelForm):
        class Meta:
            model = CategoriePatient
            fields = ['code', 'libelle', 'actif']
            widgets = {
                'code': django_forms.TextInput(attrs={'class': 'w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-clinique-bleu'}),
                'libelle': django_forms.TextInput(attrs={'class': 'w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-clinique-bleu'}),
            }

    if request.method == 'POST':
        form = CategorieForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_categories')
    else:
        form = CategorieForm()

    return render(request, 'patients/categorie_form.html', {'form': form})


@admin_clinique_required
def modifier_categorie(request, categorie_id):
    from .models import CategoriePatient
    from django import forms as django_forms

    categorie = get_object_or_404(CategoriePatient, id=categorie_id)

    class CategorieForm(django_forms.ModelForm):
        class Meta:
            model = CategoriePatient
            fields = ['code', 'libelle', 'actif']
            widgets = {
                'code': django_forms.TextInput(attrs={'class': 'w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-clinique-bleu'}),
                'libelle': django_forms.TextInput(attrs={'class': 'w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-clinique-bleu'}),
            }

    if request.method == 'POST':
        form = CategorieForm(request.POST, instance=categorie)
        if form.is_valid():
            form.save()
            return redirect('liste_categories')
    else:
        form = CategorieForm(instance=categorie)

    return render(request, 'patients/categorie_form.html', {'form': form, 'categorie': categorie})


@admin_clinique_required
def supprimer_categorie(request, categorie_id):
    from .models import CategoriePatient, Patient
    categorie = get_object_or_404(CategoriePatient, id=categorie_id)

    if request.method == 'POST':
        if Patient.objects.filter(categorie=categorie.code).exists():
            django_messages.error(request, "Cette catégorie est utilisée par des patients et ne peut pas être supprimée.")
            return redirect('liste_categories')
        categorie.delete()
        django_messages.success(request, "Catégorie supprimée.")
        return redirect('liste_categories')

    return render(request, 'patients/categorie_confirmer_suppression.html', {'categorie': categorie})
