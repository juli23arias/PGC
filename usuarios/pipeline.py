"""Pipeline personalizado para social-auth: crea el perfil de usuario automáticamente."""
from .models import Perfil


def crear_perfil_usuario(backend, user, response, *args, **kwargs):
    """Crea el Perfil del usuario si no existe al autenticarse con Google."""
    if not hasattr(user, 'perfil'):
        Perfil.objects.get_or_create(
            usuario=user,
            defaults={'rol': 'usuario'}
        )
