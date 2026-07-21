from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .decorators import admin_clinique_required
from .models import UserProfile
from .forms import CreationCompteForm


@admin_clinique_required
def liste_comptes(request):
    profiles = UserProfile.objects.select_related('user').all().order_by('user__first_name')
    return render(request, 'comptes/liste.html', {'profiles': profiles})


@admin_clinique_required
def creer_compte(request):
    if request.method == 'POST':
        form = CreationCompteForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                first_name=form.cleaned_data['prenom'],
                last_name=form.cleaned_data['nom'],
                password=form.cleaned_data['password'],
            )
            profile = user.profile
            profile.role = form.cleaned_data['role']
            profile.telephone = form.cleaned_data['telephone']
            profile.save()
            return redirect('liste_comptes')
    else:
        form = CreationCompteForm()
    return render(request, 'comptes/creer.html', {'form': form})


@admin_clinique_required
def basculer_actif_compte(request, profile_id):
    profile = get_object_or_404(UserProfile, id=profile_id)
    if profile.user != request.user:
        profile.actif = not profile.actif
        profile.user.is_active = profile.actif
        profile.user.save()
        profile.save()
    return redirect('liste_comptes')
