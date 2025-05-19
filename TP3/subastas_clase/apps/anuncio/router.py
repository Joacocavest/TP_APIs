from rest_framework import routers
from apps.anuncio.api import AnuncioViewSet, CategoriaViewSet

router = routers.DefaultRouter()
router.register(prefix='anuncio', viewset=AnuncioViewSet)

routerCategoria = routers.DefaultRouter()
routerCategoria.register(prefix='categoria', viewset=CategoriaViewSet)
