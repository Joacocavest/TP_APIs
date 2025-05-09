from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

class CustomUserAdmin(UserAdmin):
    model = Usuario
    fieldsets = UserAdmin.fieldsets + (
        ('Datos personales', {'fields': ('documento_identidad', 'domicilio')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Datos personales', {'fields': ('documento_identidad', 'domicilio')}),
    )

admin.site.register(Usuario, CustomUserAdmin)