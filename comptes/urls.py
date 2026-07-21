from django.urls import path
from . import views

urlpatterns = [
    path('', views.liste_comptes, name='liste_comptes'),
    path('creer/', views.creer_compte, name='creer_compte'),
    path('<int:profile_id>/basculer/', views.basculer_actif_compte, name='basculer_actif_compte'),
    path('<int:profile_id>/modifier/', views.modifier_compte, name='modifier_compte'),
    path('<int:profile_id>/supprimer/', views.supprimer_compte, name='supprimer_compte'),
]
