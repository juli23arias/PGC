from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Perfil


@receiver(post_save, sender=User)
def crear_perfil(sender, instance, created, **kwargs):
    if created:
        if not hasattr(instance, 'perfil'):
            rol = 'administrador' if instance.is_superuser else 'usuario'
            Perfil.objects.create(usuario=instance, rol=rol)
