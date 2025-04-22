# Para filtros aún mas avanzados, se puede especificar una clase personalizada FilterSet que desde luego
# se debe especificar en la vista para su uso

from django_filters import rest_framework as filters
from apps.anuncio.models import Categoria

class CategoriaFilter(filters.FilterSet):
    nombre = filters.CharFilter(field_name='nombre', lookup_expr='icontains')

    class Meta:
        nombre = Categoria
        fields = ['nombre',
                  'activa']