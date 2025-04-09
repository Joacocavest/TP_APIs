import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


# Base de datosenmemoria(simulación)
items = [{"id": 1, "nombre": "Laptop"}, {"id": 2, "nombre": "Telefono"}]

@csrf_exempt # Desactivala verificaciónCSRF para pruebas

def obtener_agregar_items(request): 
    if request.method== 'GET': # Devolver la lista de ítems en formatoJSON 
        return JsonResponse(items, safe=False) 
    elif request.method== 'POST': 
        try: 
            data = json.loads(request.body) # Convertir JSON en diccionario
            nuevo_item= { "id": len(items) + 1, 
            "nombre": data.get("nombre", "Sin nombre")}   
            items.append(nuevo_item) # Agregarel nuevo ítem a la lista
            return JsonResponse(nuevo_item, status=201) # Respuesta
        except json.JSONDecodeError: 
            return JsonResponse({"error": "FormatoJSON inválido"}, status=400)
        
@csrf_exempt # Desactivala verificaciónCSRF para pruebas
def buscar_item(request, item_id):
    #Buscar item por id:
    item = None
    for i in items:
        if i["id"] == item_id:
            item = i
            break

    if item == None:
        return JsonResponse({"error": "item no encontrado"}, status=404)
    
    if request.method== 'GET': # Devolver ítem en formatoJSON 
        return JsonResponse(item, safe=False)
    elif request.method == 'PUT': 
        try:
            data = json.loads(request.body) # Convertir JSON en diccionario
            item["nombre"] = data.get("nombre", item["nombre"]) #Modifica el nombre, la id no se deberia modificar
            return JsonResponse(item, status=200) # Respuesta
        except json.JSONDecodeError: #Si por algun motivo no se puede modificar, salta la exception
            return JsonResponse({"error": "FormatoJSON inválido"}, status=400)
    elif request.method == 'DELETE':
        try:
            items.remove(item) #elimina el item de la lista de items
            return JsonResponse({"mensaje": 'El item ' +item["nombre"]+ ' fue eliminado'}, status=200)
        except json.JSONDecodeError: #Si por algun motivo no se puede eliminar, salta la exception
            return JsonResponse({"error": "FormatoJSON inválido"}, status=400)
    return JsonResponse({"error": "El método HTTP no está permitido para la solicitud"}, status=405)

