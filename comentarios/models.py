from django.db import models
from django.contrib.auth.models import User
from accidentes.models import Accidente


class Comentario(models.Model):
    accidente = models.ForeignKey(
        Accidente, on_delete=models.CASCADE,
        related_name='comentarios', verbose_name='Accidente'
    )
    autor = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='comentarios', verbose_name='Autor'
    )
    contenido = models.TextField(verbose_name='Comentario')
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha')

    class Meta:
        verbose_name = 'Comentario'
        verbose_name_plural = 'Comentarios'
        ordering = ['fecha_creacion']

    def __str__(self):
        return f"Comentario de {self.autor.username} en {self.accidente.titulo}"

    def total_likes(self):
        return self.likes.count()


class Like(models.Model):
    comentario = models.ForeignKey(
        Comentario, on_delete=models.CASCADE,
        related_name='likes', verbose_name='Comentario'
    )
    usuario = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='likes', verbose_name='Usuario'
    )
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'
        unique_together = ('comentario', 'usuario')

    def __str__(self):
        return f"Like de {self.usuario.username} en comentario #{self.comentario.id}"
