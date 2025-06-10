import pytest
from django.urls import reverse
from datetime import datetime, timedelta
from django.utils.timezone import now

@pytest.mark.django_db
def test_creacion_correcta_anuncio(get_authenticated_client, get_user_generico, APIClient):
    client = get_authenticated_client

    datos_anuncio = {
        'titulo': 'Notebook de lui',
        'descripcion': 'Notebook MSI usada en buen estado',
        'precio_inicial': '3500000.00',
        'fecha_inicio': (now() + timedelta(hours=1)).isoformat(),  #dentro de 1 hora
        'fecha_fin': (now() + timedelta(days=7)).isoformat()        #dentro de 7 días
    }

    #URL de creación de anuncio
    url = reverse('anuncio-list') #name del router

    response = client.post(url, data=datos_anuncio, format='json')

    assert response.status_code == 201, response.data  # Muestra errores si falla
    data = response.data

    assert response.status_code == 201, f"Error en creación: {response.status_code} - {response.data}"

    assert data['titulo'] == datos_anuncio['titulo']
    assert data['descripcion'] == datos_anuncio['descripcion']
    assert data['precio_inicial'] == datos_anuncio['precio_inicial']
    assert data['publicado_por'] == get_user_generico.id






# @pytest.mark.django_db
# def test_creacion_fallida_anuncio_por_datos_invalidos(client, django_user_model):
#     user = django_user_model.objects.create_user(username='usuarioAux', password='hola123')
#     client.login(username='usuarioAux', password='hola123')

#     # Fecha de fin anterior a la fecha de inicio (inválido)
#     data = {
#         'titulo': '',  # título vacío
#         'descripcion': 'Sin título',
#         'fecha_inicio': timezone.now().date(),
#         'fecha_fin': timezone.now().date() - timezone.timedelta(days=1),
#     }

#     response = client.post(reverse('crear_anuncio'), data)

#     # No debería crear el anuncio
#     assert response.status_code == 200  # Si renderiza de nuevo el form con errores
#     assert Anuncio.objects.count() == 0
#     assert b'Este campo es obligatorio' in response.content or b'fecha_fin' in response.content

