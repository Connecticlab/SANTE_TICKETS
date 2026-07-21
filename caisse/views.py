from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import CaisseSession, Ticket
from .forms import EmissionTicketForm
from patients.models import Patient
from services.models import TarifService, ServiceMedical
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

    services_actifs = ServiceMedical.objects.filter(actif=True)
    services_avec_tarif = []
    for service in services_actifs:
        tarif = TarifService.objects.filter(
            service=service, categorie_patient=patient.categorie
        ).order_by('-date_effet').first()
        if tarif:
            services_avec_tarif.append({
                'service': service,
                'montant': 0 if tarif.gratuit else tarif.montant,
                'gratuit': tarif.gratuit,
            })

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

                session.recalculer_total()

                enregistrer_action(
                    utilisateur=request.user,
                    action='creation',
                    modele_cible='Ticket',
                    objet_id=ticket.numero,
                    details=f"Service: {service.nom}, Montant: {montant}",
                )

                return redirect('voir_ticket', ticket_id=ticket.id)
    else:
        form = EmissionTicketForm()

    context = {
        'patient': patient,
        'form': form,
        'erreur_tarif': erreur_tarif,
        'services_avec_tarif': services_avec_tarif,
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


@login_required
def annuler_ticket(request, ticket_id):
    profile = getattr(request.user, 'profile', None)
    est_admin_clinique = profile and profile.est_admin_clinique()

    if est_admin_clinique:
        ticket = get_object_or_404(Ticket, id=ticket_id)
    else:
        ticket = get_object_or_404(Ticket, id=ticket_id, session__caissier=request.user)

    delai_depasse = not ticket.peut_etre_annule_par_caissier()

    if ticket.statut_file == 'annule':
        return redirect('tableau_bord')

    if request.method == 'POST':
        if delai_depasse and not est_admin_clinique:
            return render(request, 'caisse/annuler_ticket.html', {
                'ticket': ticket,
                'delai_depasse': True,
                'est_admin_clinique': est_admin_clinique,
                'erreur': "Le délai de 5 minutes est dépassé. Seul l'Admin Clinique peut annuler ce ticket.",
            })

        motif = request.POST.get('motif', '').strip()
        if not motif:
            return render(request, 'caisse/annuler_ticket.html', {
                'ticket': ticket,
                'delai_depasse': False,
                'erreur': "Le motif d'annulation est obligatoire.",
            })

        ancien_montant = ticket.montant
        ticket.statut_file = 'annule'
        ticket.motif_annulation = motif
        ticket.save()

        session = ticket.session
        session.recalculer_total()

        enregistrer_action(
            utilisateur=request.user,
            action='annulation',
            modele_cible='Ticket',
            objet_id=ticket.numero,
            details=f"Motif: {motif}",
        )
        return redirect('tableau_bord')

    return render(request, 'caisse/annuler_ticket.html', {
        'ticket': ticket,
        'delai_depasse': delai_depasse,
        'est_admin_clinique': est_admin_clinique,
        'erreur': None,
    })


@login_required
@require_POST
def appeler_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, session__caissier=request.user)
    ticket.statut_file = 'appele'
    ticket.save()
    enregistrer_action(
        utilisateur=request.user,
        action='modification',
        modele_cible='Ticket',
        objet_id=ticket.numero,
        details="Ticket appele",
    )
    return redirect('tableau_bord')


def ecran_appel(request):
    ticket_appele = Ticket.objects.filter(statut_file='appele').order_by('-date').first()
    file_attente = Ticket.objects.filter(statut_file='en_attente').order_by('date')[:5]
    context = {
        'ticket_appele': ticket_appele,
        'file_attente': file_attente,
        'clinique': getattr(request, 'tenant', None),
    }
    return render(request, 'caisse/ecran_appel.html', context)


import qrcode
from io import BytesIO
from django.http import HttpResponse


@login_required
def qr_code_ticket(request, ticket_id):
    from django.urls import reverse
    ticket = get_object_or_404(Ticket, id=ticket_id)
    url_scan = request.build_absolute_uri(reverse('scanner_ticket', args=[ticket.qr_token]))
    img = qrcode.make(url_scan)
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    return HttpResponse(buffer.getvalue(), content_type='image/png')


def scanner_ticket(request, qr_token):
    ticket = get_object_or_404(Ticket, qr_token=qr_token)
    context = {
        'ticket': ticket,
        'utilisateur_connecte': request.user.is_authenticated,
    }
    return render(request, 'caisse/scan_ticket.html', context)


@login_required
def voir_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, session__caissier=request.user)
    lien_scan = request.build_absolute_uri(f'/scan/{ticket.qr_token}/')
    partage_texte = (
        f"Ticket {ticket.numero} - {request.tenant.nom_clinique if hasattr(request, 'tenant') else 'Clinique'}\n"
        f"Patient: {ticket.patient.prenom} {ticket.patient.nom}\n"
        f"Service: {ticket.service.nom}\n"
        f"Montant: {ticket.montant} FCFA\n"
        f"{lien_scan}"
    )
    return render(request, 'caisse/voir_ticket.html', {'ticket': ticket, 'partage_texte': partage_texte})


@login_required
def historique_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    tickets = Ticket.objects.filter(patient=patient).order_by('-date')
    return render(request, 'caisse/historique_patient.html', {
        'patient': patient,
        'tickets': tickets,
    })
