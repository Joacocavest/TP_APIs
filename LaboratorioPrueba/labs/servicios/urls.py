from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'usuarios', views.UsuarioViewSet)
router.register(r'servicios', views.ServicioViewSet)
router.register(r'trabajadores', views.TrabajadorViewSet)
router.register(r'contrataciones', views.ContratacionViewSet)
router.register(r'calificaciones', views.CalificacionViewSet)
router.register(r'chats', views.ChatViewSet)
router.register(r'mensajes', views.MensajeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]