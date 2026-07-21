from django.urls import path
from . import views

urlpatterns = [
    path('', views.liste_services, name='liste_services'),
    path('creer/', views.creer_service, name='creer_service'),
    path('<int:service_id>/', views.detail_service, name='detail_service'),
]
