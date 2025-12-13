from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from app.models import Producto, Categoria

def es_admin(user):
    return user.is_superuser

@login_required
@user_passes_test(es_admin)
def producto(request):
    categorias = Categoria.objects.all()
    productos = Producto.objects.select_related('categoria').all()

    edit_cat = Categoria.objects.filter(id=request.GET.get("edit_cat")).first()
    edit_prod = Producto.objects.filter(id=request.GET.get("edit_prod")).first()

    
    if "crear_producto" in request.POST:
        Producto.objects.create(
            nombre=request.POST.get('nombre', ''),
            descripcion=request.POST.get('descripcion', ''),
            precio=request.POST.get('precio', 0),
            stock=request.POST.get('stock', 0),
            marca=request.POST.get('marca', ''),
            categoria_id=request.POST.get('categoria'),
            imagen=request.POST.get("imagen")
        )
        messages.success(request, "Producto creado correctamente")
        return redirect("producto")

    if "update_producto" in request.POST:
        prod = Producto.objects.filter(id=request.POST.get("prod_id")).first()
        if prod:
            prod.nombre = request.POST.get('nombre', '')
            prod.descripcion = request.POST.get('descripcion', '')
            prod.precio = request.POST.get('precio', 0)
            prod.stock = request.POST.get('stock', 0)
            prod.marca = request.POST.get('marca', '')
            prod.categoria_id = request.POST.get('categoria')
            prod.imagen = request.POST.get("imagen")
            prod.save()
            messages.success(request, "Producto actualizado correctamente")
        return redirect("producto")

    if "eliminar_producto" in request.POST:
        Producto.objects.filter(id=request.POST.get("prod_id")).delete()
        messages.success(request, "Producto eliminado correctamente")
        return redirect("producto")

    return render(request, "producto.html", {
        "categorias": categorias,
        "productos": productos,
        "edit_cat": edit_cat,
        "edit_prod": edit_prod
    })
