import pytest
from conftest import get_user_generico, authenticated_client
from rest_framework import status
from rest_framework.test import APIClient



@pytest.mark.django_db
def test_listar_categorias(authenticated_client):
    url = 'view-set/categoria/'
    response = authenticated_client.get(url)
    assert response.status_code == status.HTTP_200_OK
