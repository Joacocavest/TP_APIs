from rest_framework.response import Response 
from rest_framework.viewsets import ViewSet
from apps.usuario.serializers import UsuarioSerializer
from apps.usuario.models import Usuario

class UsuarioViewSetV1(ViewSet):
    def list(self, request):
        usuarios = Usuario.objects.all()
        serializer = UsuarioSerializer(usuarios, many=True) 
        return Response({"mensaje": "Lista de usuarios - Versión 1", "usuarios": serializer.data})


class UsuarioViewSetV2(ViewSet):
    def list(self, request):
        return Response({"mensaje": "Lista de usuarios - Version 2 con mejoras."})
    
