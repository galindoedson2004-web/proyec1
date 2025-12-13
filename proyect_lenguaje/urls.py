"""
URL configuration for proyect_lenguaje project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app.api import api_productos, api_categorias

from app.auth_views import logindj, registerdj
from app.menu_views import menu_view, logoutdj
from app.producto_views import producto
from app.categoria_views import categoria

urlpatterns = [
    
    path('admin/', admin.site.urls),

    
    path('', menu_view, name='home'),
    path('menu/', menu_view, name='menu'),
    path('login/', logindj, name='login'),
    path('register/', registerdj, name='register'),
    path('logout/', logoutdj, name='logout'),

    
    path('producto/', producto, name='producto'),
    path('categoria/', categoria, name='categoria'),

    
    path('api/productos/', api_productos),
    path('api/categorias/', api_categorias),
]
