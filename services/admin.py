from django.contrib import admin
from .models import ServiceMedical, TarifService


class TarifServiceInline(admin.TabularInline):
    model = TarifService
    extra = 1


@admin.register(ServiceMedical)
class ServiceMedicalAdmin(admin.ModelAdmin):
    list_display = ('nom', 'code', 'actif')
    search_fields = ('nom', 'code')
    list_filter = ('actif',)
    inlines = [TarifServiceInline]


@admin.register(TarifService)
class TarifServiceAdmin(admin.ModelAdmin):
    list_display = ('service', 'categorie_patient', 'montant', 'gratuit', 'date_effet')
    list_filter = ('categorie_patient', 'gratuit')
