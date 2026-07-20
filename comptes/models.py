from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('caissier', 'Caissier'),
        ('admin_clinique', 'Admin Clinique'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='caissier')
    telephone = models.CharField(max_length=20, blank=True, null=True)
    actif = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Profil utilisateur"
        verbose_name_plural = "Profils utilisateurs"

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"

    def est_admin_clinique(self):
        return self.role == 'admin_clinique'


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def creer_profil_utilisateur(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)
