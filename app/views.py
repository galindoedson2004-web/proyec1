from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import Categoria, Producto
from django.contrib.auth.decorators import login_required,user_passes_test




# Login
def logindj(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # SI ES ADMIN → CRUD
            if user.is_superuser:
                return redirect('producto')

            # SI ES USUARIO NORMAL → MENU
            return redirect('menu')

        else:
            return render(request, 'login.html', {'error': 'Usuario o contraseña incorrectos'})
    return render(request, 'login.html')


# Registro
def registerdj(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # Validaciones
        if password1 != password2:
            return render(request, 'register.html', {'error': 'Las contraseñas no coinciden'})
        if User.objects.filter(username=email).exists():
            return render(request, 'register.html', {'error': 'Este usuario ya existe'})
        if User.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error': 'Ya se registró un usuario con este correo'})

        # Crear usuario
        user = User.objects.create_user(username=email, email=email, password=password1,
                                        first_name=first_name, last_name=last_name)
        user.save()

        #inicia sesion autoamticamente
        login(request, user)
        return redirect('menu')  #te lleva al menu

    return render(request, 'register.html')

# Menú
def menu_view(request):
    return render(request, 'menu.html')

def es_admin(user):
    return user.is_superuser

@login_required
@user_passes_test(es_admin)
def producto(request):

    categorias = Categoria.objects.all()
    productos = Producto.objects.select_related('categoria').all()

    # CARGAR DATOS PARA EDITAR
    edit_cat = Categoria.objects.filter(id=request.GET.get("edit_cat")).first()
    edit_prod = Producto.objects.filter(id=request.GET.get("edit_prod")).first()

    # ---------------------------------------
    # ----------- CATEGORÍAS ----------------
    # ---------------------------------------

    # CREAR
    if "crear_categoria" in request.POST:
        Categoria.objects.create(
            nombre=request.POST.get('nombre_cat', ''),
            descripcion=request.POST.get('descripcion_cat', ''),
            codigo=request.POST.get('codigo_cat', ''),
            seccion=request.POST.get('seccion_cat', ''),
            proveedor=request.POST.get('proveedor_cat', ''),
            garantia=request.POST.get('garantia_cat', 0)
        )
        return redirect("producto")

    # EDITAR
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
        return redirect("producto")

    # ELIMINAR
    if "eliminar_categoria" in request.POST:
        Categoria.objects.filter(id=request.POST.get("cat_id")).delete()
        return redirect("producto")

    # ---------------------------------------
    # -------------- PRODUCTOS --------------
    # ---------------------------------------

    # CREAR
    if "crear_producto" in request.POST:
        Producto.objects.create(
            nombre=request.POST.get('nombre', ''),
            descripcion=request.POST.get('descripcion', ''),
            precio=request.POST.get('precio', 0),
            stock=request.POST.get('stock', 0),
            marca=request.POST.get('marca', ''),
            categoria_id=request.POST.get('categoria')
        )
        return redirect("producto")

    # EDITAR
    if "update_producto" in request.POST:
        prod = Producto.objects.filter(id=request.POST.get("prod_id")).first()
        if prod:
            prod.nombre = request.POST.get('nombre', '')
            prod.descripcion = request.POST.get('descripcion', '')
            prod.precio = request.POST.get('precio', 0)
            prod.stock = request.POST.get('stock', 0)
            prod.marca = request.POST.get('marca', '')
            prod.categoria_id = request.POST.get('categoria')
            prod.save()
        return redirect("producto")

    # ELIMINAR
    if "eliminar_producto" in request.POST:
        Producto.objects.filter(id=request.POST.get("prod_id")).delete()
        return redirect("producto")

    return render(request, "producto.html", {
        "categorias": categorias,
        "productos": productos,
        "edit_cat": edit_cat,
        "edit_prod": edit_prod
    })
