from functools import wraps
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages


def admin_clinique_required(view_func):
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        profile = getattr(request.user, 'profile', None)
        if not (profile and profile.est_admin_clinique()):
            messages.error(request, "Accès réservé à l'Admin Clinique.")
            return redirect('tableau_bord')
        return view_func(request, *args, **kwargs)
    return wrapper
