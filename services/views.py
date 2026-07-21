from django.shortcuts import render, redirect, get_object_or_404
from comptes.decorators import admin_clinique_required
from .models import ServiceMedical, TarifService
from .forms import ServiceMedicalForm, TarifServiceForm


@admin_clinique_required
def liste_services(request):
    services = ServiceMedical.objects.all().order_by('nom')
    return render(request, 'services/liste.html', {'services': services})


@admin_clinique_required
def creer_service(request):
    if request.method == 'POST':
        form = ServiceMedicalForm(request.POST)
        if form.is_valid():
            service = form.save()
            return redirect('detail_service', service_id=service.id)
    else:
        form = ServiceMedicalForm()
    return render(request, 'services/creer.html', {'form': form})


@admin_clinique_required
def detail_service(request, service_id):
    from django.db import IntegrityError
    service = get_object_or_404(ServiceMedical, id=service_id)
    tarifs = service.tarifs.all().order_by('-date_effet')
    erreur = None

    if request.method == 'POST':
        form = TarifServiceForm(request.POST)
        if form.is_valid():
            tarif = form.save(commit=False)
            tarif.service = service
            try:
                tarif.save()
                return redirect('detail_service', service_id=service.id)
            except IntegrityError:
                erreur = "Un tarif existe deja pour cette categorie de patient a cette date. Modifiez la date d'effet ou le tarif existant."
    else:
        form = TarifServiceForm()

    return render(request, 'services/detail.html', {
        'service': service,
        'tarifs': tarifs,
        'form': form,
        'erreur': erreur,
    })


from django.contrib import messages as django_messages
from django.db.models import ProtectedError


@admin_clinique_required
def supprimer_service(request, service_id):
    service = get_object_or_404(ServiceMedical, id=service_id)

    if request.method == 'POST':
        try:
            service.delete()
            django_messages.success(request, "Service supprimé.")
            return redirect('liste_services')
        except ProtectedError:
            django_messages.error(request, "Ce service a des tickets associés et ne peut pas être supprimé. Désactivez-le plutôt.")
            return redirect('detail_service', service_id=service.id)

    return render(request, 'services/confirmer_suppression.html', {'service': service})


@admin_clinique_required
def modifier_tarif(request, tarif_id):
    tarif = get_object_or_404(TarifService, id=tarif_id)

    if request.method == 'POST':
        form = TarifServiceForm(request.POST, instance=tarif)
        if form.is_valid():
            form.save()
            return redirect('detail_service', service_id=tarif.service.id)
    else:
        form = TarifServiceForm(instance=tarif)

    return render(request, 'services/modifier_tarif.html', {'form': form, 'tarif': tarif})
