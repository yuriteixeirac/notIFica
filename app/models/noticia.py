from django.db import models
from app.models import Usuario


class Noticia(models.Model):
    class Meta:
        ordering = ['-data']
        db_table = 'noticia'

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    titulo = models.CharField(max_length=200)
    sumario = models.TextField()

    link = models.URLField(null=True, max_length=512)

    imagem = models.URLField(null=True, max_length=512)
    data = models.DateTimeField(auto_now_add=True)

    em_display = models.BooleanField(default=True)
    automatizada = models.BooleanField(default=False)
