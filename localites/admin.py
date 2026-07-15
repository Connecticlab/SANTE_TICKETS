from django.contrib import admin
from .models import Localite


@admin.register(Localite)
class LocaliteAdmin(admin.ModelAdmin):
    list_display = ('nom', 'commune', 'actif')
    search_fields = ('nom',)
    list_filter = ('actif',)
