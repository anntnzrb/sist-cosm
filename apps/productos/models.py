from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator


class Producto(models.Model):
    IVA_CHOICES = [
        (15, '15%'),
        (0, '0%'),
    ]
    
    nombre = models.CharField(max_length=200, verbose_name="Nombre")
    descripcion = models.TextField(verbose_name="Descripción")
    precio = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], verbose_name="Precio")
    iva = models.IntegerField(choices=IVA_CHOICES, verbose_name="IVA")
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True, verbose_name="Imagen")
    
    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre
    
    def get_precio_con_iva(self):
        return self.precio * (1 + self.iva / 100)
    
    def get_absolute_url(self):
        return reverse('productos:detail', kwargs={'pk': self.pk})
