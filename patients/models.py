import uuid
from django.db import models
from localites.models import Localite


class CategoriePatient(models.Model):
    code = models.CharField(max_length=30, unique=True, help_text="Identifiant technique (ex: ordinaire)")
    libelle = models.CharField(max_length=100, help_text="Nom affiche (ex: Ordinaire)")
    actif = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Categorie de patient"
        verbose_name_plural = "Categories de patient"
        ordering = ['libelle']

    def __str__(self):
        return self.libelle


class Patient(models.Model):
    CATEGORIE_CHOICES = [
        ('ordinaire', 'Ordinaire'),
        ('mutualiste', 'Mutualiste'),
        ('indigent', 'Indigent'),
    ]

    numero_patient = models.CharField(max_length=30, unique=True, editable=False)
    nom = models.CharField(max_length=150)
    prenom = models.CharField(max_length=150)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    date_naissance = models.DateField(blank=True, null=True)
    categorie = models.CharField(max_length=20, choices=CATEGORIE_CHOICES, default='ordinaire')
    qr_code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    quartier_village = models.ForeignKey(
        Localite,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='patients',
    )
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Patient"
        verbose_name_plural = "Patients"
        ordering = ['-date_creation']

    def get_categorie_libelle(self):
        categorie = CategoriePatient.objects.filter(code=self.categorie).first()
        return categorie.libelle if categorie else self.get_categorie_display()

    def save(self, *args, **kwargs):
        if not self.numero_patient:
            # Généré à la première sauvegarde : préfixe + timestamp compact
            from django.utils import timezone
            self.numero_patient = f"PAT-{timezone.now().strftime('%y%m%d%H%M%S')}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.numero_patient} — {self.prenom} {self.nom}"
