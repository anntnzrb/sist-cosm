from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError
from datetime import datetime


class Empresa(models.Model):
    nombre = models.CharField(max_length=200, verbose_name="Nombre")
    direccion = models.TextField(verbose_name="Dirección")
    mision = models.TextField(verbose_name="Misión")
    vision = models.TextField(verbose_name="Visión")
    anio_fundacion = models.IntegerField(verbose_name="Año de fundación")
    ruc = models.CharField(max_length=20, unique=True, verbose_name="RUC")
    imagen = models.ImageField(upload_to='empresa/', blank=True, null=True, verbose_name="Imagen")
    
    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresa"
    
    def __str__(self):
        return self.nombre
    
    def save(self, *args, **kwargs):
        if not self.pk and Empresa.objects.exists():
            raise ValidationError("Solo puede existir una empresa en el sistema")
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('empresa:detail')
    
    @property
    def anos_experiencia(self):
        """Calcula los años de experiencia desde la fundación hasta la fecha actual"""
        current_year = datetime.now().year
        return current_year - self.anio_fundacion
