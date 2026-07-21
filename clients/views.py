from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from .models import Client, Domain


@staff_member_required
def console_super_admin(request):
    cliniques = Client.objects.exclude(schema_name='public').order_by('-date_creation')

    stats = {
        'total_actives': cliniques.filter(actif=True).count(),
        'total_cliniques': cliniques.count(),
    }

    cliniques_avec_domaine = []
    for clinique in cliniques:
        domaine = clinique.domains.filter(is_primary=True).first()
        cliniques_avec_domaine.append({
            'clinique': clinique,
            'domaine': domaine,
        })

    context = {
        'cliniques_avec_domaine': cliniques_avec_domaine,
        'stats': stats,
    }
    return render(request, 'clients/console.html', context)


from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from .forms import OnboardingCliniqueForm


@staff_member_required
def ajouter_clinique(request):
    if request.method == 'POST':
        form = OnboardingCliniqueForm(request.POST)
        if form.is_valid():
            from .models import Domain
            from django_tenants.utils import schema_context

            client = Client.objects.create(
                schema_name=form.cleaned_data['schema_name'],
                nom_clinique=form.cleaned_data['nom_clinique'],
                plan_abonnement=form.cleaned_data['plan_abonnement'],
                actif=True,
            )

            Domain.objects.create(
                domain=f"{form.cleaned_data['sous_domaine']}.santickets.mairiesokone.com",
                tenant=client,
                is_primary=True,
            )

            with schema_context(client.schema_name):
                from django.contrib.auth.models import User
                from comptes.models import UserProfile

                admin_user = User.objects.create_user(
                    username=form.cleaned_data['admin_username'],
                    first_name=form.cleaned_data['admin_prenom'],
                    last_name=form.cleaned_data['admin_nom'],
                    password=form.cleaned_data['admin_password'],
                )
                profile = admin_user.profile
                profile.role = 'admin_clinique'
                profile.save()

            messages.success(request, f"Clinique '{client.nom_clinique}' créée avec succès. Compte Admin Clinique : {form.cleaned_data['admin_username']}")
            return redirect('console_super_admin')
    else:
        form = OnboardingCliniqueForm()

    return render(request, 'clients/ajouter.html', {'form': form})
