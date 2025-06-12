#Preparacion de un test para tener en cuenta

# =====================================================================
# @pytest.mark.django_db  # Parte 1
# def test_algo(client, user):  # Parte 2
#     # Parte 3: Preparación de datos
#     data = {...}

#     # Parte 4: Acción
#     response = client.post("/api/algo/", data)

#     # Parte 5: Verificación
#     assert response.status_code == 201
#     assert response.data["nombre"] == data["nombre"]
# =====================================================================


import pytest
from django.utils import timezone
from django.urls import reverse
from apps.anuncio.models import Anuncio, Categoria

@pytest.mark.django_db
def test_creacion_anuncio(get_authenticated_client, get_user_generico):
    categoria = Categoria.objects.create(nombre = 'Tecnologia', activa = True) #Creamos una categoria primero que es necesaria para la creacion del Anuncio

    #Asignamos los datos de entrada para el anuncio creado
    data = {
        "titulo": "Producto de Prueba",
        "descripcion": "Descripción de prueba para testing",
        "precio_inicial": "100000.00",
        "fecha_inicio": (timezone.now() + timezone.timedelta(days=1)).isoformat(),
        "fecha_fin": (timezone.now() + timezone.timedelta(days=7)).isoformat(),
        "categorias": [categoria.id]
    }

    #Debemos realizar la solicitud Post en este caso para la creacion al edpoint
    response = get_authenticated_client.post(reverse('anuncio-list'), data, format = 'json')


    #Verificamos que se creo correctamente
    assert response.status_code == 201

    #Para conocer el contenido de la respuesta
    respuesta = response.data
    assert respuesta ['titulo'] == data['titulo']
    assert float(respuesta['precio_inicial']) == float(data["precio_inicial"])

    # Verificamos que se guardó en la base de datos
    anuncio = Anuncio.objects.get(id=respuesta['id'])
    assert anuncio.publicado_por == get_user_generico
    assert categoria in anuncio.categorias.all()

@pytest.mark.django_db
def test_creacion_anuncio_invalido(get_authenticated_client):
    categoria = Categoria.objects.create(nombre='Tecnología', activa=True)

    # Faltan campos obligatorios como 'titulo' y 'precio_inicial'
    data = {
        "descripcion": "Intento de anuncio sin título ni precio",
        "fecha_inicio": (timezone.now() + timezone.timedelta(days=1)).isoformat(),
        "fecha_fin": (timezone.now() + timezone.timedelta(days=7)).isoformat(),
        "categorias": [categoria.id]
    }

    url = reverse('anuncio-list')
    response = get_authenticated_client.post(url, data, format='json')

    print("STATUS:", response.status_code)
    print("DATA:", response.data)

    assert response.status_code == 400
    assert 'titulo' in response.data
    assert 'precio_inicial' in response.data

@pytest.mark.django_db
def test_listar_categoria(get_categorias, get_authenticated_client, get_user_generico):
    response = get_authenticated_client.get(reverse('categoria-list'),format='json')
    assert response.status_code == 200
    assert str(cat['nombre'] == get_categorias.nombre for cat in response.data)

@pytest.mark.django_db
def test_listar_anuncios(get_authenticated_client, get_user_generico):
    response = get_authenticated_client.get(reverse('anuncio-list'), format='json')
    assert response.status_code == 200

    resultado = response.data['results']
    assert isinstance(resultado, list)

    print("ANUNCIOS EN LA BD:", resultado)


# @pytest.mark.django_db
# def test_api_crear_anuncio_falla_fecha_inicio_anterior_actual(mocker, get_authenticated_client, get_categoria):
#     from datetime import datetime, timedelta, timezone
#     # Simulamos que “la fecha actual (ahora)" es 2025-06-12 12:00:00
#     fecha_actual_mock = datetime(2025, 6, 12, 12, 0, 0, tzinfo=timezone.utc)

#     mocker.patch('django.utils.timezone.now', return_value=fecha_actual_mock)

#     data = {
#         "titulo": "Mesa living",
#         "descripcion": "Mesa ratona de living con vidrio",
#         "precio_inicial": "150500.00",
#         "fecha_inicio": fecha_actual_mock - timedelta(days=1), # un día antes del "ahora" simulado
#         "fecha_fin": fecha_actual_mock + timedelta(days=5),
#         "categorias": [get_categoria.id]
#     }
#     cliente = get_authenticated_client
#     response = cliente.post(reverse('anuncio-list'), data=data)
#     assert response.status_code == 400
#     assert str(response.data['fecha_inicio'][0]) == "La Fecha de Inicio no puede ser anterior a la Fecha Actual."