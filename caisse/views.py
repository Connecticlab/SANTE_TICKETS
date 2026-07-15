from django.shortcuts import render
from .models import CaisseSession, Ticket


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
