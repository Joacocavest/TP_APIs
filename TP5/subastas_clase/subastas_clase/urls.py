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
###################################################
#        TP5
from rest_framework.authtoken.views import obtain_auth_token

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
#####path del TP5######
    path('api-token-auth/', obtain_auth_token,)
]

# Trabajo Practico N°5
# Justificación del uso de Token Authentication:
    # Se elige el esquema Token Authentication por lo siguiente:
    # Ofrece más seguridad que la autenticación básica, porque no se envían las credenciales con cada solicitud, sino un token que genera el servidor.
    # Es más sencilla de implementar que JWT o OAuth 2.0, sobre todo para APIs internas o proyectos de complejidad media como el del sistema de subastas.
    # Permite una gestión sencilla de los tokens, la revocación o la regeneración se puede realizar desde la base de datos (modelo Token de DRF).
    # Es adecuada para autenticación sin estado (stateless), y para su uso con clientes móviles, SPA o integraciones simples.
    # No requiere infraestructura adicional (servidores de autorización para OAuth) y tampoco la firma de tokens como sucede con JWT, lo cual acorta el tiempo de desarrollo.