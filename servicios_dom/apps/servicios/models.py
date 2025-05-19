from django.db import models

# Create your models here.
class Servicio(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def str(self):
        return self.nombre