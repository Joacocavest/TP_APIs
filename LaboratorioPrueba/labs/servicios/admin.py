from django.contrib import admin
from .models import Usuario, Servicio, Trabajador, Contratacion, Calificacion, Chat, Mensaje

admin.site.register(Usuario)
admin.site.register(Servicio)
admin.site.register(Trabajador)
admin.site.register(Contratacion)
admin.site.register(Calificacion)
admin.site.register(Chat)
admin.site.register(Mensaje)
