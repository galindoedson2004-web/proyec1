from django.http import JsonResponse

# API REST: PRODUCTOS
from django.http import JsonResponse
from .models import Producto, Categoria

def api_productos(request):
    productos = list(Producto.objects.values(
        "id", "nombre", "descripcion", "precio", "stock", "marca", "categoria_id"
    ))
    return JsonResponse(productos, safe=False, json_dumps_params={'indent': 4})

def api_categorias(request):
    categorias = list(Categoria.objects.values(
        "id", "nombre", "descripcion", "codigo", "seccion", "proveedor", "garantia"
    ))
    return JsonResponse(categorias, safe=False, json_dumps_params={'indent': 4})
