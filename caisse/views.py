from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import CaisseSession, Ticket


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
