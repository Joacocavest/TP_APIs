from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.anuncio.models import Anuncio, Categoria
from apps.anuncio.serializers import AnuncioSerializer, CategoriaSerializer
from apps.usuario.models import Usuario

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
                