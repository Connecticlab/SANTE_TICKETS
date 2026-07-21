from django.urls import path
from . import views

urlpatterns = [
    path('', views.tableau_bord_caissier, name='tableau_bord'),
    path('tickets/', views.liste_tickets, name='liste_tickets'),
    path('sessions/', views.vue_sessions, name='vue_sessions'),
    path('sessions/<int:session_id>/', views.detail_session, name='detail_session'),
    path('session/ouvrir/', views.ouvrir_session, name='ouvrir_session'),
    path('session/cloturer/', views.cloturer_session, name='cloturer_session'),
    path('ticket/nouveau/<int:patient_id>/', views.nouveau_ticket, name='nouveau_ticket'),
    path('ticket/voir/<int:ticket_id>/', views.voir_ticket, name='voir_ticket'),
    path('ticket/annuler/<int:ticket_id>/', views.annuler_ticket, name='annuler_ticket'),
    path('ticket/appeler/<int:ticket_id>/', views.appeler_ticket, name='appeler_ticket'),
    path('ticket/qr/<int:ticket_id>/', views.qr_code_ticket, name='qr_code_ticket'),
    path('salle-attente/', views.ecran_appel, name='ecran_appel'),
    path('scan/<uuid:qr_token>/', views.scanner_ticket, name='scanner_ticket'),
    path('historique/<int:patient_id>/', views.historique_patient, name='historique_patient'),
]
