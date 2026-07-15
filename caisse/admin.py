from django.contrib import admin
from .models import CaisseSession, Ticket


@admin.register(CaisseSession)
class CaisseSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'caissier', 'date_ouverture', 'date_cloture', 'total', 'statut', 'sync_status')
    list_filter = ('statut', 'sync_status')


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('numero', 'patient', 'service', 'montant', 'statut_file', 'statut_paiement', 'date')
    search_fields = ('numero', 'patient__nom', 'patient__prenom')
    list_filter = ('statut_file', 'statut_paiement')
