from django.urls import path
from . import views

urlpatterns = [
    path('', views.liste_patients_view, name='liste_patients'),
    path('rechercher/', views.rechercher_patient_view, name='rechercher_patient'),
    path('creer/', views.creer_patient_view, name='creer_patient'),
    path('categories/', views.liste_categories, name='liste_categories'),
    path('categories/creer/', views.creer_categorie, name='creer_categorie'),
    path('categories/<int:categorie_id>/modifier/', views.modifier_categorie, name='modifier_categorie'),
    path('categories/<int:categorie_id>/supprimer/', views.supprimer_categorie, name='supprimer_categorie'),
    path('<int:patient_id>/', views.detail_patient_view, name='detail_patient'),
    path('<int:patient_id>/supprimer/', views.supprimer_patient_view, name='supprimer_patient'),
    path('qr/<int:patient_id>/', views.qr_code_patient, name='qr_code_patient'),
    path('scan/', views.scanner_patient, name='scanner_patient'),
]
