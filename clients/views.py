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
