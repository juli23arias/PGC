from django.db import models
from django.contrib.auth.models import User


class Accidente(models.Model):
    GRAVEDAD_CHOICES = (
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta'),
    )

    titulo = models.CharField(max_length=200, verbose_name='Título')
    ubicacion = models.CharField(max_length=300, verbose_name='Ubicación')
    descripcion = models.TextField(verbose_name='Descripción')
    gravedad = models.CharField(max_length=10, choices=GRAVEDAD_CHOICES, verbose_name='Gravedad')
    fecha = models.DateTimeField(verbose_name='Fecha del accidente')
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de registro')
    reportado_por = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='accidentes', verbose_name='Reportado por'
    )
    latitud = models.FloatField(null=True, blank=True, verbose_name='Latitud')
    longitud = models.FloatField(null=True, blank=True, verbose_name='Longitud')
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Accidente'
        verbose_name_plural = 'Accidentes'
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.titulo} - {self.get_gravedad_display()} ({self.fecha.strftime('%d/%m/%Y')})"

    def get_gravedad_color(self):
        colores = {
            'baja': 'success',
            'media': 'warning',
            'alta': 'danger',
        }
        return colores.get(self.gravedad, 'secondary')

    def get_gravedad_icon(self):
        iconos = {
            'baja': 'bi-check-circle',
            'media': 'bi-exclamation-triangle',
            'alta': 'bi-x-circle',
        }
        return iconos.get(self.gravedad, 'bi-circle')

    def get_gravedad_color_hex(self):
        colores = {
            'baja': '#22c55e',
            'media': '#f59e0b',
            'alta': '#ef4444',
        }
        return colores.get(self.gravedad, '#6b7280')

    def tiene_coordenadas(self):
        return self.latitud is not None and self.longitud is not None
