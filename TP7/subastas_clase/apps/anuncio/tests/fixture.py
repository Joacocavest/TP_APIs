import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse


User = get_user_model()

def create_user(username, documento_identidad, first_name = 'Micaela', last_name = 'Salgado', password='unpassword',    email = None):

    email='{}@root.com'.format(username) if email is None else email            
    user, created = User.objects.get_or_create(username=username, email=email)

    if created:
        user.documento_identidad = documento_identidad
        user.first_name = first_name
        user.last_name = last_name
        user.is_active = True
        user.set_password(password) # Se Hashea la contraseña al guardarla en la BD user.save()
        user.save()
    return user

@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def get_user_generico():
    test_user = create_user(username='test_user', documento_identidad='44635875', first_name='Test', last_name='User', email='test@user.com')
    return test_user


@pytest.fixture
def get_authenticated_client(get_user_generico):
    client = APIClient()

    #URL del endpoint de obtención del token JWT
    url = reverse('token_obtain_pair')

    response = client.post(url, {
        'username': get_user_generico.username,
        'password': 'unpassword'
    })

    assert response.status_code == 200
    access_token = response.data['access']

    #Configuramos el header Authorization con el JWT
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    return client


