from rest_framework.response import Response 
from rest_framework.viewsets import ViewSet

class UsuarioViewSetV1(ViewSet):
    def list(self, request):
        return Response({"mensaje": "Lista de usuarios - Version 1"})
    

class UsuarioViewSetV2(ViewSet):
    def list(self, request):
        return Response({"mensaje": "Lista de usuarios - Version 2 con mejoras."})
    
