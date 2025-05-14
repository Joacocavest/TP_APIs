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

class CategoriaAPIView(APIView):
    #defino el metodo get para devolver la lista de categorias cuando la solicitud proviene del metodo get
    def get(self, request, format=None):
        categorias = Categoria.objects.all()
        #una vez tengo la lista de categorias las tengo que devolver serializadas.
        serializer = CategoriaSerializer(categorias, many=True)
        return Response(serializer.data) #El atributo "data" devuelve los datos serializados. Response convierte los datos en tipo python en tipo JSON
    
    #Cuando los datos vienen por el metodo post, tenemos que recibir los datos, serializarlos, validarlos y guardarlos.
    def post(self, request, format=None):
        serializer = CategoriaSerializer(data=request.data) #Al enviar "data" como parametro, estamos deserializando ya que la data vino en formato JSON(objeto request.data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)#Envio los datos serializados o deserializados y el codigo de estado
        #Si el serializador no es valid devolvemos:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

#Vista con CRUD para una instancia de categoria especifica(id)
class CategoriaDetalleAPIView(APIView):
    #Cuando nos llegue el pk(id), busco esa categoria, la serializamos, y devolvemos
    def get(self, request, pk):
        categoria = get_object_or_404(Categoria, pk=pk) #Con esta funcion get_object_or_404 nos ahorramos la tarea de hacer un bloque try-except 
        serialize = CategoriaSerializer(categoria)
        return Response(serialize.data)
    
    #Cuando nos llegue el pk(id), busco ese anuncio, lo serializamos, validamos, guardamos y devolvemos
    def put(self, request, pk):
        categoria = get_object_or_404(Categoria, pk=pk) #Con esta funcion get_object_or_404 nos ahorramos la tarea de hacer un bloque try-except 
        serialize = CategoriaSerializer(categoria, data=request.data)
        if serialize.is_valid():
            serialize.save()
            return Response(serialize.data)
        return Response(serialize.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        categoria = get_object_or_404(Categoria, pk=pk) #Con esta funcion get_object_or_404 nos ahorramos la tarea de hacer un bloque try-except
        categoria.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





class AnunciosAPIView(APIView):
    #Si la peticion viene por el metodo get, muestro la lista de anuncios
    def get(self, request, format=None):
        anuncios = Anuncio.objects.all()
        #una vez tengo la lista de anuncios los tengo que devolver serializados.
        serialize = AnuncioSerializer(anuncios, many=True)
        return Response(serialize.data)
    
    def post(self, request, format=None):
        serialize = AnuncioSerializer(data=request.data) #Al enviar "data" como parametro, estamos deserializando ya que la data vino en formato JSON(objeto request.data)
        if serialize.is_valid():
            usuario = Usuario.objects.first()
            serialize.save(publicado_por=usuario)
            return Response(serialize.data, status=status.HTTP_201_CREATED)
        return Response(serialize.errors, status=status.HTTP_400_BAD_REQUEST)
    

class AnuncioDetalleAPIView(APIView):
    #Cuando nos llegue el pk(id), busco ese anuncio, lo serializamos, y devolvemos
    def get(self, request, pk):
        anuncio = get_object_or_404(Anuncio, pk=pk) #Con esta funcion get_object_or_404 nos ahorramos la tarea de hacer un bloque try-except 
        serialize = AnuncioSerializer(anuncio)
        return Response(serialize.data)
    
    #Cuando nos llegue el pk(id), busco ese anuncio, lo serializamos, validamos, guardamos y devolvemos
    def put(self, request, pk):
        anuncio = get_object_or_404(Anuncio, pk=pk)
        serialize = AnuncioSerializer(anuncio, data=request.data) #Al enviar "data" como parametro, estamos deserializando ya que la data vino en formato JSON(objeto request.data)
        if serialize.is_valid():
            serialize.save()
            return Response(serialize.data)
        return Response(serialize.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #Cuando nos llegue el pk(id), busco ese anuncio, lo eliminamos y devolvemos
    def delete(self, request, pk):
        anuncio = get_object_or_404(Anuncio, pk=pk)
        anuncio.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    




####################################################################################################################################################################################
#                                                    TRABAJO PRACTICO N°3                                                                                                          #
####################################################################################################################################################################################





################################
#ENDPOINTS CON VISTAS GENERICAS#
################################


#Lista de categorias
class CategoriaListaGenericView(ListCreateAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

#Detalle de una categoria
class CategoriaDetalleGenericView(RetrieveUpdateDestroyAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer



#Lista de anuncios
class ListaAnunciosGenericView(ListCreateAPIView):
    queryset = Anuncio.objects.all()
    serializer_class = AnuncioSerializer

#detalle de un anuncio
class DetalleAnuncioGenericView(RetrieveUpdateDestroyAPIView):
    queryset = Anuncio.objects.all()
    serializer_class = AnuncioSerializer





################################
#ENDPOINTS CON VISTAS VIEWSET#
################################

#CRUD Categoria
class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
#######################################################################
#                           TPN°4                                     #
#######################################################################
# Filtros en el API:

# Uso de DjangoFilterBackend
#Si solo se necesita hacer un filtrado simple, por igualdad de algún campo del modelo,
#se puede establecer un atributo filterset_fields en la vista, indicando los campos a filtrar
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    #filterset_fields = ['nombre', 'activa']
#Si se especifica una clase de filtro ya no se usan los filterset_fields, se usa:
    filterset_class = CategoriaFilter

#Uso de OrderingFilter:
#OrderingFilter proviene del paquete "rest_framework.filters", admite la ordenacion de los resultados controlada por los parametros de la consulta.
#Se recomienda especificar explicitamente por cuales campos se va a ordenar el resultado
    ordering_fields = ['nombre', 'activa']

#La forma más simple de filtrar el conjunto de consultas de cualquier vista que herede de
# GenericAPIView es sobrescribir el método get_queryset()
    def get_queryset(self):
        return Categoria.objects.filter(nombre__istartwith='c')

#FILTRADO DE OBJETOS SOBRESCRIBIENDO EL MÉTODO GET_QUERYSET Y TOMANDO PARÁMETROS
#DE LA CONSULTA
    def get_queryset(self):
        queryset = Categoria.objects.all()
        nombre = self.request.query_params.get('nombre', None)
        if nombre is not None:
            queryset= queryset.filter(nombre=nombre)
        return queryset


#CRUD Anuncio
class AnuncioViewSet(viewsets.ModelViewSet):
    queryset = Anuncio.objects.all()
    serializer_class = AnuncioSerializer
    #####################
# Uso de DjangoFilterBackend
#Si solo se necesita hacer un filtrado simple, por igualdad de algún campo del modelo,
#se puede establecer un atributo filterset_fields en la vista, indicando los campos a filtrar
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = AnuncioFilter
# Uso de OrderingFilter:
#OrderingFilter proviene del paquete "rest_framework.filters", admite la ordenacion de los resultados controlada por los parametros de la consulta.
#Se recomienda especificar explicitamente por cuales campos se va a ordenar el resultado
    ordering_fields = ['titulo', 'fecha_inicio', 'fecha_fin']

#### T      TPN5        ###
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return AnuncioReadSerializer
        return AnuncioSerializer

# Por el momento, en ambos casos forzar la asignación de un usuario (Considerar sobrescribir el método “perform_create” 
# para asignar un usuario cuando se crea un anuncio).

    def perform_create(self, serializer):
        #Asignar el usuario con id=1
        #usuario = Usuario.objects.get(id=1)
        serializer.save(publicado_por=self.request.user)


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

##Filtros basicos

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
