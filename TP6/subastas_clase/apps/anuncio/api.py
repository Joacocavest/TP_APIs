from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, filters
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.generics import get_object_or_404, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from apps.anuncio.models import Anuncio, Categoria
from apps.anuncio.serializers import AnuncioReadSerializer, AnuncioSerializer, CategoriaSerializer, OfertaSerializer
from apps.usuario.models import Usuario
from rest_framework.decorators import action
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from apps.anuncio.filters import AnuncioFilter, CategoriaFilter
from apps.anuncio.permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

#-----------------------------------------------------------------------------
#ENDPOINTS CON VISTAS VIEWSET
# Filtros en el API:
#Si solo se necesita hacer un filtrado simple, por igualdad de algún campo del modelo,
#se puede establecer un atributo filterset_fields en la vista, indicando los campos a filtrar
#Si se especifica una clase de filtro ya no se usan los filterset_fields, se usa filterset_class
#--------------------------------------------------------------------------
#Uso de OrderingFilter:
#OrderingFilter proviene del paquete "rest_framework.filters", admite la ordenacion de los resultados controlada 
#por los parametros de la consulta.Se recomienda especificar explicitamente por cuales campos se va a ordenar el resultado
#La forma más simple de filtrar el conjunto de consultas de cualquier vista que herede de
# GenericAPIView es sobrescribir el método get_queryset()
#FILTRADO DE OBJETOS SOBRESCRIBIENDO EL MÉTODO GET_QUERYSET Y TOMANDO PARÁMETROS DE LA CONSULTA
#--------------------------------------------------------------------------
#CRUD Categoria
class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer    
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = CategoriaFilter
    ordering_fields = ['nombre', 'activa']

    def get_queryset(self):
        return Categoria.objects.filter(nombre__istartwith='c')

    def get_queryset(self):
        queryset = Categoria.objects.all()
        nombre = self.request.query_params.get('nombre', None) #busca si en la URL del request hay un parámetro llamado nombre por ej: /api/categorias/?nombre=Computadoras
        if nombre is not None:
            queryset= queryset.filter(nombre=nombre) #Se filtran las categorías devolviendo solo las que tengan exactamente ese nombre.
        return queryset


#CRUD Anuncio
class AnuncioViewSet(viewsets.ModelViewSet):
    queryset = Anuncio.objects.all()
    serializer_class = AnuncioSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = AnuncioFilter
    ordering_fields = ['titulo', 'fecha_inicio', 'fecha_fin']
#--------------------------------------------------------------------------
    #authentication_classes=[SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        #Asignar el usuario con id=1
        #usuario = Usuario.objects.get(id=1)
        serializer.save(publicado_por=self.request.user)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return AnuncioReadSerializer
        return AnuncioSerializer


#Accion personalizada que devuelve el timepo restante
#solo es para lectura por el cual utilizamos el metodo 'get', la accion se le aplica a un objeto en este caso un anuncio
    @action(detail=True, methods=['get']) 
    def tiempo_restante(self, request, pk=None):
        anuncio = self.get_object()
        if anuncio.fecha_fin:
            ahora = timezone.now()
            restante = anuncio.fecha_fin - ahora
            dias = restante.days
            horas, resto = divmod(restante.seconds, 3600)
            minutos, _ = divmod(resto, 60)
            return Response({
                'días': dias,
                'horas': horas,
                'minutos': minutos
            })
        return Response({"mensaje": "El anuncio no tiene una fecha de fin definida."})
#filtrado de anuncios por titulo
    def get_queryset(self):
        queryset = Anuncio.objects.all()
        titulo = self.request.query_params.get('titulo', None)
        if titulo is not None:
            queryset = queryset.filter(titulo=titulo)
        return queryset
    

    @extend_schema(
        summary="Saludo simple",
        description="Este endpoint devuelve un mensaje de saludo.",
        responses={200: str}
    )
    
    def get(self, request):
        return Response("Hola Mundo")


    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def ofertar(self, request, pk=None):
            anuncio = self.get_object()

            # No permitir si el anuncio no está activo
            if not anuncio.activo:
                return Response({"error": "El anuncio no está activo."}, status=status.HTTP_400_BAD_REQUEST)

            # No permitir que el creador oferte
            if anuncio.publicado_por == request.user:
                return Response({"error": "No podés ofertar en tu propio anuncio."}, status=status.HTTP_403_FORBIDDEN)

            serializer = OfertaSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(anuncio=anuncio, usuario=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def ofertas(self, request, pk=None):
        anuncio = self.get_object()
        ofertas = anuncio.ofertas.all()
        serializer = OfertaSerializer(ofertas, many=True)
        return Response(serializer.data)
    
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return AnuncioReadSerializer
        return AnuncioSerializer
