from django.db import models
from app.models import Usuario

class Postagem(models.Model):
    class Meta:
        ordering = ['-data']
        db_table = 'postagem'
    
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    corpo = models.CharField(max_length=324)

    imagem = models.URLField(max_length=512, null=True)
    data = models.DateTimeField(auto_now_add=True)
