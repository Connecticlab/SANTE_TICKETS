from django.shortcuts import render, redirect
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
