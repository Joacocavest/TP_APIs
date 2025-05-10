from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Solo el propietario del anuncio puede modificarlo o eliminarlo.
    Otros usuarios solo pueden ver.
    """

    def has_object_permission(self, request, view, obj):
        # Los métodos seguros (GET, HEAD, OPTIONS) se permiten a todos
        if request.method in permissions.SAFE_METHODS:
            return True

        # Solo permite modificar/eliminar si el usuario autenticado es el creador
        return obj.publicado_por == request.user
