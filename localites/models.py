from django.db import models


class Localite(models.Model):
    nom = models.CharField(max_length=150)
    commune = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='quartiers',
        help_text="Commune parente (optionnel, pour la hiérarchie quartier/village -> commune)",
    )
    actif = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Localité"
        verbose_name_plural = "Localités"
        ordering = ['nom']

    def __str__(self):
        if self.commune:
            return f"{self.nom} ({self.commune.nom})"
        return self.nom
