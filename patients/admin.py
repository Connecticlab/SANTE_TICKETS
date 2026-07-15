from django.contrib import admin
from .models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('numero_patient', 'nom', 'prenom', 'telephone', 'categorie', 'date_creation')
    search_fields = ('numero_patient', 'nom', 'prenom', 'telephone')
    list_filter = ('categorie',)
