from django.db import models
from patients.models import Patient


class ServiceMedical(models.Model):
    nom = models.CharField(max_length=150)
    code = models.CharField(max_length=30, unique=True)
    description = models.TextField(blank=True)
    actif = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Service médical"
        verbose_name_plural = "Services médicaux"
        ordering = ['nom']

    def __str__(self):
        return f"{self.nom} ({self.code})"


class TarifService(models.Model):
    service = models.ForeignKey(ServiceMedical, on_delete=models.CASCADE, related_name='tarifs')
    categorie_patient = models.CharField(max_length=20, choices=Patient.CATEGORIE_CHOICES)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    gratuit = models.BooleanField(default=False)
    date_effet = models.DateField()

    class Meta:
        verbose_name = "Tarif de service"
        verbose_name_plural = "Tarifs de service"
        ordering = ['-date_effet']
        # Un seul tarif "actuel" par service+categorie a une date d'effet donnee
        constraints = [
            models.UniqueConstraint(
                fields=['service', 'categorie_patient', 'date_effet'],
                name='unique_tarif_service_categorie_date',
            )
        ]

    def __str__(self):
        if self.gratuit:
            return f"{self.service.nom} — {self.categorie_patient} — Gratuit"
        return f"{self.service.nom} — {self.categorie_patient} — {self.montant} FCFA"
