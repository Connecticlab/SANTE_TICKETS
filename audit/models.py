from django.conf import settings
from django.db import models


class JournalAudit(models.Model):
    ACTION_CHOICES = [
        ('creation', 'Création'),
        ('modification', 'Modification'),
        ('annulation', 'Annulation'),
    ]

    utilisateur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='actions_audit',
    )
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    modele_cible = models.CharField(max_length=100, help_text="Nom du modèle concerné (ex: Ticket, Patient)")
    objet_id = models.CharField(max_length=50, help_text="Identifiant de l'objet concerné")
    date_heure = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True, help_text="Détails de l'action (motif, anciennes/nouvelles valeurs...)")

    class Meta:
        verbose_name = "Entrée du journal d'audit"
        verbose_name_plural = "Journal d'audit"
        ordering = ['-date_heure']

    def __str__(self):
        return f"[{self.date_heure:%Y-%m-%d %H:%M}] {self.utilisateur} — {self.action} sur {self.modele_cible}#{self.objet_id}"


def enregistrer_action(utilisateur, action, modele_cible, objet_id, details=""):
    """Fonction utilitaire pour journaliser une action sensible depuis n'importe quelle app."""
    return JournalAudit.objects.create(
        utilisateur=utilisateur,
        action=action,
        modele_cible=modele_cible,
        objet_id=str(objet_id),
        details=details,
    )
