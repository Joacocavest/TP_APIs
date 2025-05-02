from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

class Usuario(AbstractUser):
    es_trabajador = models.BooleanField(default=False)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)

    # Especificamos related_name únicos para evitar conflictos
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='usuario_set',
        blank=True,
        help_text='Los grupos a los que pertenece este usuario.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='usuario_set',
        blank=True,
        help_text='Permisos específicos para este usuario.',
        verbose_name='user permissions',
    )
class Servicio(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    
    def __str__(self):
        return self.nombre

class Trabajador(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    calificacion_promedio = models.FloatField(default=0)
    total_calificaciones = models.IntegerField(default=0)
    
    def actualizar_calificacion(self):
        calificaciones = Calificacion.objects.filter(trabajador=self)
        if calificaciones.count() >= 10:
            self.calificacion_promedio = calificaciones.aggregate(models.Avg('estrellas'))['estrellas__avg']
            self.save()

class Contratacion(models.Model):
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('EN_PROCESO', 'En Proceso'),
        ('COMPLETADO', 'Completado'),
        ('CANCELADO', 'Cancelado')
    ]
    
    cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='contrataciones_cliente')
    trabajador = models.ForeignKey(Trabajador, on_delete=models.CASCADE)
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='PENDIENTE')
    direccion_servicio = models.CharField(max_length=255)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    
    def get_monto_dolares(self):
        try:
            response = requests.get('https://dolarapi.com/v1/dolares/blue')
            data = response.json()
            valor_dolar = float(data['venta'])
            return round(float(self.monto) / valor_dolar, 2)
        except Exception:
            return None

class Calificacion(models.Model):
    contratacion = models.OneToOneField(Contratacion, on_delete=models.CASCADE)
    trabajador = models.ForeignKey(Trabajador, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    estrellas = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comentario = models.TextField(blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

class Chat(models.Model):
    cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='chats_cliente')
    trabajador = models.ForeignKey(Trabajador, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

class Mensaje(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='mensajes')
    emisor = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)