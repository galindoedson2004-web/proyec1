from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from app.models import Categoria

def es_admin(user):
    return user.is_superuser

@login_required
@user_passes_test(es_admin)
def categoria(request):
    categorias = Categoria.objects.all()
    edit_cat = Categoria.objects.filter(id=request.GET.get("edit_cat")).first()

    if "crear_categoria" in request.POST:
        Categoria.objects.create(
            nombre=request.POST.get('nombre_cat', ''),
            descripcion=request.POST.get('descripcion_cat', ''),
            codigo=request.POST.get('codigo_cat', ''),
            seccion=request.POST.get('seccion_cat', ''),
            proveedor=request.POST.get('proveedor_cat', ''),
            garantia=request.POST.get('garantia_cat', 0)
        )
        messages.success(request, "Categoria creada correctamente")
        return redirect("categoria")

    if "update_categoria" in request.POST:
        cat = Categoria.objects.filter(id=request.POST.get("cat_id")).first()
        if cat:
            cat.nombre = request.POST.get('nombre_cat', '')
            cat.descripcion = request.POST.get('descripcion_cat', '')
            cat.codigo = request.POST.get('codigo_cat', '')
            cat.seccion = request.POST.get('seccion_cat', '')
            cat.proveedor = request.POST.get('proveedor_cat', '')
            cat.garantia = request.POST.get('garantia_cat', 0)
            cat.save()
            messages.success(request, "Categoria actualizada correctamente")
        return redirect("categoria")

    if "eliminar_categoria" in request.POST:
        Categoria.objects.filter(id=request.POST.get("cat_id")).delete()
        messages.success(request, "Categoria eliminada correctamente")
        return redirect("categoria")

    return render(request, 'categoria.html', {
        'categorias': categorias,
        'edit_cat': edit_cat
    })
