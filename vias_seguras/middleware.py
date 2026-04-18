"""Middleware: requiere autenticación para todas las vistas excepto las públicas."""
from django.shortcuts import redirect
from django.conf import settings

URLS_PUBLICAS = [
    '/usuarios/login/',
    '/usuarios/registro/',
    '/auth/',          # social auth (Google OAuth)
    '/admin/',         # Django admin
    '/static/',
    '/media/',
    '/favicon.ico',
]

class LoginRequeridoMiddleware:
    """Redirige a login si el usuario no está autenticado."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Verificar si la URL actual comienza con alguna URL pública
        path = request.path_info
        es_publica = any(path.startswith(url) for url in URLS_PUBLICAS)

        if not es_publica and not request.user.is_authenticated:
            login_url = settings.LOGIN_URL
            return redirect(f'{login_url}?next={path}')

        return self.get_response(request)
