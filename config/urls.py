from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('console/', include('clients.urls')),
    path('patients/', include('patients.urls')),
    path('services/', include('services.urls')),
    path('comptes/', include('comptes.urls')),
    path('localites/', include('localites.urls')),
    path('', include('caisse.urls')),
]
