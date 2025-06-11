import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'subastas_clase.settings')
django.setup()

# import pytest
# from rest_framework.test import APIClient
# from django.contrib.auth import get_user_model
# from django.urls import reverse
# from rest_framework_simplejwt.tokens import RefreshToken
# from django.contrib.auth import get_user_model

# User = get_user_model()

# def create_user(username, documento_identidad, first_name='Micaela', last_name='Salgado', password='unpassword', email=None):
#     email = f'{username}@root.com' if email is None else email
#     user, created = User.objects.get_or_create(username=username, email=email)
#     if created:
#         user.documento_identidad = documento_identidad
#         user.first_name = first_name
#         user.last_name = last_name
#         user.is_active = True
#         user.set_password(password)
#         user.save()
#     return user

# @pytest.fixture
# def get_user_generico():
#     return create_user(username='test_user', documento_identidad='44635875')

# @pytest.fixture
# def authenticated_client(get_user_generico):
#     client = APIClient()
#     refresh = RefreshToken.for_user(get_user_generico)
#     access_token = str(refresh.access_token)
#     client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
#     return client


import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken



User = get_user_model()

def create_user(username, documento_identidad, first_name='Guille', last_name='Joaco', password='unpassword', email=None):
    email = '{}@root.com'.format(username) if email is None else email
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
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def get_user_generico():
    user = create_user(username='userTest', documento_identidad='44635875', first_name='usuarioTest', last_name='userTestt', email='test@user.com')
    return user

@pytest.fixture
def authenticated_client(get_user_generico, api_client):
    client = api_client()
    refresh = RefreshToken.for_user(get_user_generico)
    access_token = str(refresh.access_token)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    return client