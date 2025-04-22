from rest_framework import serializers
from django.utils import timezone
from .models import Anuncio, Categoria


class CategoriaSerializer(serializers.ModelSerializer): 
    class Meta: 
        model= Categoria
        fields= [
            'id',
            'nombre',
            'activa',
        ]

#######################################################################
#                           TPN°4                                     #
#######################################################################

    #validaciones personalizadas a nivel de "field"
    def validate_nombre(self, value):
            #Verificar que el nombre no contenga la palabra "categoria"
            if "categoria" in value.lower():
                raise serializers.ValidationError("El nombre no puede contener la palabra 'categoria'.")
            return value
        
    #Validaciones personalizadas a nivel de "Object", metodo "validate()", recibe como argumento un diccionario de valores de los fields
    def validate(self, data):
            if 'principal' in data['nombre'].lower() and not data['activa']:
                raise serializers.ValidationError("No se puede desactivar la categoria principal")
            return data

########################################################################

class AnuncioReadSerializer(serializers.ModelSerializer):
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
            'fecha_fin',
            'activo',
            'categorias',
            'publicado_por',
            'oferta_ganadora',
        ]
        read_only_fields = ['publicado_por', 'oferta_ganadora']

class AnuncioSerializer(serializers.ModelSerializer):
    #categorias = serializers.StringRelatedField(many=True)
    categorias = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Categoria.objects.all()
    )
    publicado_por = serializers.StringRelatedField()
    class Meta:
        model=Anuncio
        fields= [
            'id',
            'titulo',
            'precio_inicial',
            'fecha_publicacion',
            'fecha_inicio',
            'fecha_fin',
            'activo',
            'categorias',
            'publicado_por',
            'oferta_ganadora',
        ]
        read_only_fields = ['publicado_por', 'oferta_ganadora']




#######################################################################
#                           TPN°4                                     #
#######################################################################    

####Validaciones

    def validate_fecha_inicio(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("La fecha de inicio debe ser posterior a hoy.")
        return value

    def validate(self, data):
        fecha_inicio = data.get("fecha_inicio")
        fecha_fin = data.get("fecha_fin")

        if fecha_fin and fecha_inicio <= fecha_inicio:
            raise serializers.ValidationError("La fecha de fin debe ser posterior a la de inicio.")
        return data


##Filtros basicos

def get_queryset(self):
    queryset = Anuncio.objects.all()
    titulo = self.request.query_params.get('titulo', None)
    if titulo is not None:
        queryset = queryset.filter(titulo=titulo)
    return queryset
