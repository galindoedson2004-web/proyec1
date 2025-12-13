from django.shortcuts import render, redirect
from django.contrib.auth import logout
from app.models import Producto

def menu_view(request):
    productos = Producto.objects.all()
    return render(request, 'menu.html', {'productos': productos})

def logoutdj(request):
    logout(request)
    return redirect('login')
