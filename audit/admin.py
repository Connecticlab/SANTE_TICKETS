from django.contrib import admin
from .models import JournalAudit


@admin.register(JournalAudit)
class JournalAuditAdmin(admin.ModelAdmin):
    list_display = ('date_heure', 'utilisateur', 'action', 'modele_cible', 'objet_id')
    list_filter = ('action', 'modele_cible')
    search_fields = ('objet_id', 'details')
    readonly_fields = ('utilisateur', 'action', 'modele_cible', 'objet_id', 'date_heure', 'details')

    def has_add_permission(self, request):
        # Le journal ne doit jamais etre modifie manuellement, seulement genere par l'application
        return False

    def has_delete_permission(self, request, obj=None):
        return False
