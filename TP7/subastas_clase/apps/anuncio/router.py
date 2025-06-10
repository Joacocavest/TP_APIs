from rest_framework import routers
from apps.anuncio.api import AnuncioViewSet

router = routers.DefaultRouter()
router.register(prefix='anuncio', viewset=AnuncioViewSet, basename='anuncio')
