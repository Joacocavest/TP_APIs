from rest_framework import serializers
from apps.usuario.models import Usuario
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
    categorias = serializers.StringRelatedField(many=True)
    publicado_por = serializers.StringRelatedField()
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


