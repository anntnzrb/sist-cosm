from django.db import models
from django.urls import reverse


class Trabajador(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    apellido = models.CharField(max_length=100, verbose_name="Apellido")
    correo = models.EmailField(verbose_name="Correo electrónico")
    cedula = models.CharField(max_length=20, unique=True, verbose_name="Cédula")
    codigo_empleado = models.CharField(max_length=20, unique=True, verbose_name="Código de empleado")
    imagen = models.ImageField(upload_to='trabajadores/', blank=True, null=True, verbose_name="Imagen")
    
    class Meta:
        verbose_name = "Trabajador"
        verbose_name_plural = "Trabajadores"
        ordering = ['nombre', 'apellido']
    
    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
    def get_absolute_url(self):
        return reverse('trabajadores:detail', kwargs={'pk': self.pk})
