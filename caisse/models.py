import uuid
from django.conf import settings
from django.db import models
from django.utils import timezone
from patients.models import Patient
from services.models import ServiceMedical


class CaisseSession(models.Model):
    STATUT_CHOICES = [
        ('ouverte', 'Ouverte'),
        ('cloturee', 'Clôturée'),
    ]

    caissier = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='sessions_caisse')
    date_ouverture = models.DateTimeField(auto_now_add=True)
    date_cloture = models.DateTimeField(null=True, blank=True)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='ouverte')
    sync_status = models.CharField(
        max_length=20,
        choices=[('synchronise', 'Synchronisé'), ('en_attente', 'En attente de synchronisation')],
        default='synchronise',
    )

    class Meta:
        verbose_name = "Session de caisse"
        verbose_name_plural = "Sessions de caisse"
        ordering = ['-date_ouverture']

    def recalculer_total(self):
        total = self.tickets.exclude(statut_file='annule').aggregate(
            somme=models.Sum('montant')
        )['somme'] or 0
        self.total = total
        self.save()
        return self.total

    def cloturer(self):
        self.recalculer_total()
        self.statut = 'cloturee'
        self.date_cloture = timezone.now()
        self.save()

    def __str__(self):
        return f"Session {self.id} — {self.caissier} — {self.statut}"


class Ticket(models.Model):
    STATUT_FILE_CHOICES = [
        ('en_attente', 'En attente'),
        ('appele', 'Appelé'),
        ('traite', 'Traité'),
        ('annule', 'Annulé'),
    ]
    STATUT_PAIEMENT_CHOICES = [
        ('paye', 'Payé'),
        ('en_attente_remboursement', 'En attente remboursement'),
        ('gratuit_indigent', 'Gratuit — indigent'),
    ]

    numero = models.CharField(max_length=30, unique=True, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT, related_name='tickets')
    service = models.ForeignKey(ServiceMedical, on_delete=models.PROTECT, related_name='tickets')
    session = models.ForeignKey(CaisseSession, on_delete=models.PROTECT, related_name='tickets')
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    statut_file = models.CharField(max_length=20, choices=STATUT_FILE_CHOICES, default='en_attente')
    statut_paiement = models.CharField(max_length=30, choices=STATUT_PAIEMENT_CHOICES, default='paye')
    qr_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    motif_annulation = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Ticket"
        verbose_name_plural = "Tickets"
        ordering = ['-date']

    def save(self, *args, **kwargs):
        if not self.numero:
            dernier = Ticket.objects.order_by('-id').first()
            prochain_id = (dernier.id + 1) if dernier else 1
            self.numero = f"TK-{prochain_id:04d}"
        super().save(*args, **kwargs)

    def peut_etre_annule_par_caissier(self, delai_minutes=5):
        """CDC §7.2 etape 13 : annulation caissier autorisee dans les 5 minutes suivant l'emission."""
        ecart = timezone.now() - self.date
        return ecart.total_seconds() <= delai_minutes * 60

    def __str__(self):
        return f"{self.numero} — {self.patient} — {self.statut_file}"
