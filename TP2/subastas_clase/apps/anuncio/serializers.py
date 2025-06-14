from rest_framework import serializers
from .models import Anuncio, Categoria


class CategoriaSerializer(serializers.ModelSerializer): 
    class Meta: 
        model= Categoria
        fields= [
            'id',
            'nombre',
            'activa',
        ]


class AnuncioSerializer(serializers.ModelSerializer):
    categorias = serializers.PrimaryKeyRelatedField(queryset=Categoria.objects.all(), many=True) #Deja enviar el id de la categoria cuando el metodo es POST
    #categorias = serializers.StringRelatedField(many=True) #StringRelatedField es solo de lectura, no deja enviar categorias cuando el metodo es POST en la vista
    class Meta:
        model=Anuncio
        fields= [
            'id',
            'titulo',
            'precio_inicial',
            'fecha_publicacion',
            'fecha_inicio',
            'activo',
            'categorias',
            'publicado_por',
            'oferta_ganadora',
        ]
        read_only_fields = ['publicado_por', 'oferta_ganadora']

