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


from django.contrib import messages
from .forms import ModifierCompteForm


@admin_clinique_required
def modifier_compte(request, profile_id):
    profile = get_object_or_404(UserProfile, id=profile_id)

    if request.method == 'POST':
        form = ModifierCompteForm(request.POST)
        if form.is_valid():
            profile.user.first_name = form.cleaned_data['prenom']
            profile.user.last_name = form.cleaned_data['nom']
            profile.user.save()
            profile.role = form.cleaned_data['role']
            profile.telephone = form.cleaned_data['telephone']
            profile.save()

            nouveau_mdp = form.cleaned_data.get('nouveau_mot_de_passe')
            if nouveau_mdp:
                profile.user.set_password(nouveau_mdp)
                profile.user.save()
                messages.success(request, "Compte mis à jour et mot de passe réinitialisé.")
            else:
                messages.success(request, "Compte mis à jour.")

            return redirect('liste_comptes')
    else:
        form = ModifierCompteForm(initial={
            'nom': profile.user.last_name,
            'prenom': profile.user.first_name,
            'telephone': profile.telephone,
            'role': profile.role,
        })

    return render(request, 'comptes/modifier.html', {'form': form, 'profile': profile})


@admin_clinique_required
def supprimer_compte(request, profile_id):
    profile = get_object_or_404(UserProfile, id=profile_id)

    if profile.user == request.user:
        messages.error(request, "Vous ne pouvez pas supprimer votre propre compte.")
        return redirect('liste_comptes')

    if request.method == 'POST':
        from django.db.models import ProtectedError
        try:
            profile.user.delete()
            messages.success(request, "Compte supprimé.")
            return redirect('liste_comptes')
        except ProtectedError:
            messages.error(request, "Ce compte a des sessions de caisse associées et ne peut pas être supprimé. Désactivez-le à la place.")
            return redirect('liste_comptes')

    return render(request, 'comptes/confirmer_suppression.html', {'profile': profile})
