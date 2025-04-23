"""
URL configuration for subastas_clase project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from django.urls import include, path
from apps.usuario.api import UsuarioViewSetV1, UsuarioViewSetV2
from apps.anuncio.api import AnuncioViewSetV1

router_v1 = DefaultRouter()
router_v1.register(r'usuarios', UsuarioViewSetV1, basename='usuarios-v1')

router_v2 = DefaultRouter()
router_v2.register(r'usuarios', UsuarioViewSetV2, basename='usuarios-v2')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.anuncio.urls', namespace='anuncio')),
#####path del TP3######
    path('view-set/', include('subastas_clase.router')),

#####path del TP4######
    path('api/v1/', include(router_v1.urls)),
    path('api/v2/', include(router_v2.urls)),

]
