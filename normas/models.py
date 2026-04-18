from django.db import models


class NormaTransito(models.Model):
    CATEGORIAS = (
        ('velocidad', 'Velocidad'),
        ('senales', 'Señales de tránsito'),
        ('alcoholemia', 'Alcoholemia'),
        ('peatones', 'Peatones'),
        ('motocicletas', 'Motocicletas'),
        ('documentos', 'Documentos'),
        ('infracciones', 'Infracciones'),
        ('general', 'General'),
    )

    titulo = models.CharField(max_length=200, verbose_name='Título')
    descripcion = models.TextField(verbose_name='Descripción')
    categoria = models.CharField(max_length=30, choices=CATEGORIAS, verbose_name='Categoría')
    articulo = models.CharField(max_length=100, blank=True, null=True, verbose_name='Artículo')
    activo = models.BooleanField(default=True, verbose_name='Activo')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Norma de Tránsito'
        verbose_name_plural = 'Normas de Tránsito'
        ordering = ['categoria', 'titulo']

    def __str__(self):
        return f"{self.titulo} ({self.get_categoria_display()})"

    def get_categoria_icon(self):
        iconos = {
            'velocidad': 'bi-speedometer2',
            'senales': 'bi-sign-stop',
            'alcoholemia': 'bi-cup',
            'peatones': 'bi-person-walking',
            'motocicletas': 'bi-bicycle',
            'documentos': 'bi-file-text',
            'infracciones': 'bi-exclamation-octagon',
            'general': 'bi-book',
        }
        return iconos.get(self.categoria, 'bi-book')

    def get_categoria_color(self):
        colores = {
            'velocidad': 'danger',
            'senales': 'primary',
            'alcoholemia': 'warning',
            'peatones': 'success',
            'motocicletas': 'info',
            'documentos': 'secondary',
            'infracciones': 'dark',
            'general': 'primary',
        }
        return colores.get(self.categoria, 'primary')
