from django.urls import path
from . import views

urlpatterns = [
    path('', views.console_super_admin, name='console_super_admin'),
]
