from django.db import models
from django_tenants.models import TenantMixin, DomainMixin


class Client(TenantMixin):
    nom_clinique = models.CharField(max_length=255)
    date_creation = models.DateField(auto_now_add=True)
    plan_abonnement = models.CharField(
        max_length=50,
        choices=[
            ('essai', 'Essai gratuit'),
            ('standard', 'Standard'),
            ('premium', 'Premium'),
        ],
        default='essai',
    )
    actif = models.BooleanField(default=True)

    # Le schema est créé automatiquement à la sauvegarde
    auto_create_schema = True

    def __str__(self):
        return self.nom_clinique


class Domain(DomainMixin):
    pass
