from django.urls import path
from . import views

urlpatterns = [
    path('rechercher/', views.rechercher_patient_view, name='rechercher_patient'),
    path('creer/', views.creer_patient_view, name='creer_patient'),
]
