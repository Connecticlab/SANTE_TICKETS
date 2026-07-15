from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('', views.tableau_bord_caissier, name='tableau_bord'),
    path('session/ouvrir/', views.ouvrir_session, name='ouvrir_session'),
]
