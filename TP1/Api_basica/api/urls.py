from django.urls import path
from .views import buscar_item, obtener_agregar_items

urlpatterns= [    
    path('items/', obtener_agregar_items, name='obtener_agregar_items'),
    path('item/<int:item_id>/', buscar_item, name='buscar_item'),
]




