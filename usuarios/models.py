from django.db import models
from django.contrib.auth.models import User


class Perfil(models.Model):
    ROLES = (
        ('usuario', 'Usuario'),
        ('administrador', 'Administrador'),
    )
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    rol = models.CharField(max_length=20, choices=ROLES, default='usuario')
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'

    def __str__(self):
        return f"{self.usuario.username} - {self.get_rol_display()}"

    def es_administrador(self):
        return self.rol == 'administrador'
