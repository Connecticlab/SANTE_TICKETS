from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import ProtectedError
from comptes.decorators import admin_clinique_required
from .models import Localite
from .forms import LocaliteForm


@admin_clinique_required
def liste_localites(request):
    localites = Localite.objects.all().order_by('nom')
    return render(request, 'localites/liste.html', {'localites': localites})


@admin_clinique_required
def creer_localite(request):
    if request.method == 'POST':
        form = LocaliteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_localites')
    else:
        form = LocaliteForm()
    return render(request, 'localites/creer.html', {'form': form})


@admin_clinique_required
def modifier_localite(request, localite_id):
    localite = get_object_or_404(Localite, id=localite_id)
    if request.method == 'POST':
        form = LocaliteForm(request.POST, instance=localite)
        if form.is_valid():
            form.save()
            return redirect('liste_localites')
    else:
        form = LocaliteForm(instance=localite)
    return render(request, 'localites/creer.html', {'form': form, 'localite': localite})


@admin_clinique_required
def supprimer_localite(request, localite_id):
    localite = get_object_or_404(Localite, id=localite_id)
    if request.method == 'POST':
        try:
            localite.delete()
            messages.success(request, "Localité supprimée.")
        except ProtectedError:
            messages.error(request, "Cette localité est utilisée par des patients et ne peut pas être supprimée.")
        return redirect('liste_localites')
    return render(request, 'localites/confirmer_suppression.html', {'localite': localite})
