from django.urls import path

from apps.anuncio.api import AnuncioDetalleAPIView, AnunciosAPIView, CategoriaAPIView, CategoriaDetalleAPIView


app_name = 'anuncio'

urlpatterns = [
    path('api-view/categoria/', CategoriaAPIView.as_view()),
    path('api-view/categoria/<int:pk>/', CategoriaDetalleAPIView.as_view()),
    path('api-view/anuncio/', AnunciosAPIView.as_view()),
    path('api-view/anuncio/<int:pk>', AnuncioDetalleAPIView.as_view()),
]