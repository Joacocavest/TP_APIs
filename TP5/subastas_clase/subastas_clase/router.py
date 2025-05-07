from rest_framework import routers

from apps.anuncio.api import AnuncioViewSet, CategoriaViewSet


#Inicializar el router de DRF solo una vez
router = routers.DefaultRouter()

#Registrar viewset de categoria
router.register(prefix='categoria', viewset=CategoriaViewSet)

#Registrar viewset de anuncio
router.register(prefix='anuncio', viewset=AnuncioViewSet)

urlpatterns = router.urls