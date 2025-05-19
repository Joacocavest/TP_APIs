from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    TIPO = [
        ('cliente', 'Cliente'),
        ('trabajador', 'Trabajador')
    ]

    tipo = models.CharField(max_length=20, choices=TIPO)
    domicilio= models.CharField(max_length=250, blank=True, unique=True)
    servicio = models.ForeignKey(
        'apps.servicio.Servicio',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return f'{self.username} - ({self.tipo})'










