from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import CaisseSession, Ticket
from .forms import EmissionTicketForm
from patients.models import Patient
from services.models import TarifService
from audit.models import enregistrer_action


@login_required
def tableau_bord_caissier(request):
    session = CaisseSession.objects.filter(
        caissier=request.user, statut='ouverte'
    ).first()

    tickets = []
    if session:
        tickets = session.tickets.order_by('-date')[:10]

    context = {
        'session': session,
        'tickets': tickets,
    }
    return render(request, 'caisse/tableau_bord.html', context)


@login_required
@require_POST
def ouvrir_session(request):
    session_existante = CaisseSession.objects.filter(
        caissier=request.user, statut='ouverte'
    ).first()
    if not session_existante:
        CaisseSession.objects.create(caissier=request.user)
    return redirect('tableau_bord')


@login_required
def nouveau_ticket(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    session = CaisseSession.objects.filter(
        caissier=request.user, statut='ouverte'
    ).first()

    if not session:
        return redirect('tableau_bord')

    erreur_tarif = None

    if request.method == 'POST':
        form = EmissionTicketForm(request.POST)
        if form.is_valid():
            service = form.cleaned_data['service']
            tarif = TarifService.objects.filter(
                service=service, categorie_patient=patient.categorie
            ).order_by('-date_effet').first()

            if not tarif:
                erreur_tarif = "Aucun tarif défini pour ce service et cette catégorie de patient."
            else:
                montant = 0 if tarif.gratuit else tarif.montant
                statut_paiement = 'gratuit_indigent' if tarif.gratuit else 'paye'

                ticket = Ticket.objects.create(
                    patient=patient,
                    service=service,
                    session=session,
                    montant=montant,
                    statut_paiement=statut_paiement,
                )

                session.total = session.total + montant
                session.save()

                enregistrer_action(
                    utilisateur=request.user,
                    action='creation',
                    modele_cible='Ticket',
                    objet_id=ticket.numero,
                    details=f"Service: {service.nom}, Montant: {montant}",
                )

                return redirect('tableau_bord')
    else:
        form = EmissionTicketForm()

    context = {
        'patient': patient,
        'form': form,
        'erreur_tarif': erreur_tarif,
    }
    return render(request, 'caisse/nouveau_ticket.html', context)


@login_required
@require_POST
def cloturer_session(request):
    session = CaisseSession.objects.filter(
        caissier=request.user, statut='ouverte'
    ).first()
    if session:
        session.cloturer()
        enregistrer_action(
            utilisateur=request.user,
            action='modification',
            modele_cible='CaisseSession',
            objet_id=session.id,
            details=f"Cloture de session, total: {session.total} FCFA",
        )
    return redirect('tableau_bord')
