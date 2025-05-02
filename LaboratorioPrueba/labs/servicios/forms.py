from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario

class RegistroForm(UserCreationForm):
    direccion = forms.CharField(max_length=255)
    telefono = forms.CharField(max_length=20)
    es_trabajador = forms.BooleanField(required=False)

    class Meta:
        model = Usuario
        fields = ('username', 'email', 'password1', 'password2', 'direccion', 'telefono', 'es_trabajador')