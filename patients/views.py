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
