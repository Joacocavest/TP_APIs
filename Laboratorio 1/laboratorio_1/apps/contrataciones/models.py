from django.db import models

# Create your models here.

class contratacion(models.Model):
    ESTADO = [                             #revisar
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('finalizada', 'Finalizada')
    ]

    cliente = models.ForeignKey('apps.usuario.User', related_name='contrataciones', on_delete=models.CASCADE, unique=True)
    trabajador = models.ForeignKey('apps.usuario.User', related_name='trabajos', on_delete=models.CASCADE, unique=True)
    servicio = models.ForeignKey('apps.servicio.Servicio', on_delete=models.CASCADE, unique=True)
    direccion = models.CharField(max_length=250, blank=False, unique=True)
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADO, default='pendiente')

    def __str__(self):
        return f'{self.servicio.nombre} - {self.cliente.username} - {self.trabajador.username} - {self.estado}'
