from django.urls import path
from . import views

urlpatterns = [
    path('', views.tableau_bord_caissier, name='tableau_bord'),
    path('session/ouvrir/', views.ouvrir_session, name='ouvrir_session'),
    path('session/cloturer/', views.cloturer_session, name='cloturer_session'),
    path('ticket/nouveau/<int:patient_id>/', views.nouveau_ticket, name='nouveau_ticket'),
    path('ticket/annuler/<int:ticket_id>/', views.annuler_ticket, name='annuler_ticket'),
]
