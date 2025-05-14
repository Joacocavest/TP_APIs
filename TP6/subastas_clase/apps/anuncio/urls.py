from django.urls import path, include
from .router import router
from apps.anuncio.api import AnuncioDetalleAPIView, AnunciosAPIView, CategoriaAPIView, CategoriaDetalleAPIView, CategoriaDetalleGenericView, CategoriaListaGenericView, DetalleAnuncioGenericView, ListaAnunciosGenericView


app_name = 'anuncio'

urlpatterns = [
    path('api-view/categoria/', CategoriaAPIView.as_view()),
    path('api-view/categoria/<int:pk>/', CategoriaDetalleAPIView.as_view()),
    path('api-view/anuncio/', AnunciosAPIView.as_view()),
    path('api-view/anuncio/<int:pk>', AnuncioDetalleAPIView.as_view()),

#PATH del tp3:

    path('generic-view/categoria/', CategoriaListaGenericView.as_view()),
    path('generic-view/categoria/<int:pk>', CategoriaDetalleGenericView.as_view()),
    path('generic-view/anuncio/', ListaAnunciosGenericView.as_view()),
    path('generic-view/anuncio/<int:pk>', DetalleAnuncioGenericView.as_view()),

    path('view-set/', include(router.urls)),
]