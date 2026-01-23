from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    class Meta:
        db_table = 'usuario'
    
    email = models.EmailField(unique=True, null=False)
    is_servidor = models.BooleanField(default=False)


    @property
    def is_authorized(self):
        return self.is_servidor


    def __str__(self):
        return self.username
