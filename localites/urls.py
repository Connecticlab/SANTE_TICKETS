from django.urls import path
from . import views

urlpatterns = [
    path('', views.liste_localites, name='liste_localites'),
    path('creer/', views.creer_localite, name='creer_localite'),
    path('<int:localite_id>/modifier/', views.modifier_localite, name='modifier_localite'),
    path('<int:localite_id>/supprimer/', views.supprimer_localite, name='supprimer_localite'),
]
