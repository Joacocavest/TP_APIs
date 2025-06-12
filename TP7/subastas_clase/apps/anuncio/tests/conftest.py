
#Preparacion de un fixture para tener en cuenta
# ================================================================

# @pytest.fixture
# def mi_fixture():
#     # 1. Preparación
#     objeto = {"nombre": "prueba", "valor": 123}

#     # 2. Retorno
#     return objeto

# ================================================================


import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from apps.anuncio.models import Categoria, Anuncio

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

def create_user(username, documento_identidad = '44582654', first_name='Micaela', last_name='Salgado', password='unpassword', email=None):

    email = f'{username}@root.com' if email is None else email
    user, created = User.objects.get_or_create(username=username, email=email)
    if created:
        user.documento_identidad = documento_identidad
        user.first_name = first_name
        user.last_name = last_name
        user.is_active = True
        user.set_password(password)
        user.save()
    return user

@pytest.fixture
def get_user_generico():
    return create_user(username='test_user')

@pytest.fixture
def get_authenticated_client(get_user_generico, api_client):

    refresh = RefreshToken.for_user(get_user_generico)
    access_token = str(refresh.access_token)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    return api_client

@pytest.fixture
def get_categorias():
    categoria1 = Categoria.objects.get_or_create(
        nombre = 'Papeleo',
        defaults = {
            'activa': True
        }
    )
    categoria2, _ = Categoria.objects.get_or_create(
        nombre='Electronica',
        defaults={
        "activa": True
        }
        )
    categoria3, _ = Categoria.objects.get_or_create(
    nombre='Hogar',
    defaults={
        "activa": False
    }
    )

    return categoria1, categoria2, categoria3