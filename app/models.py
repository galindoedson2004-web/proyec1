from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=70)
    descripcion = models.TextField()
    codigo = models.CharField(max_length=100)
    seccion = models.CharField(max_length=40)
    proveedor = models.CharField(max_length=20)
    garantia = models.IntegerField()
    

    def __str__(self):
        return self.nombre
    
class Producto(models.Model):
    nombre = models.CharField(max_length=70)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    marca = models.CharField(max_length=20)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    imagen = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.nombre
    

