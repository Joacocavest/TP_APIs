# Para filtros aún mas avanzados, se puede especificar una clase personalizada FilterSet que desde luego
# se debe especificar en la vista para su uso

from django_filters import rest_framework as filters
from apps.anuncio.models import Anuncio, Categoria

class CategoriaFilter(filters.FilterSet):
    nombre = filters.CharFilter(field_name='nombre', lookup_expr='icontains')

    class Meta:
        model = Categoria
        fields = ['nombre',
                  'activa']
        

class AnuncioFilter(filters.FilterSet):
    titulo = filters.CharFilter(field_name='titulo', lookup_expr='icontains')
    fecha_inicio = filters.DateFromToRangeFilter(field_name='fecha_inicio')
    fecha_fin = filters.DateFromToRangeFilter(field_name='fecha_fin')
    categorias = filters.CharFilter(field_name='categoria', lookup_expr='icontains')
    class Meta:
        model = Anuncio
        fields = [
            'titulo',
            'fecha_inicio',
            'fecha_fin',
        ]