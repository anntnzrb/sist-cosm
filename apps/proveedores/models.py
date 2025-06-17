from django.db import models
from django.urls import reverse


class Proveedor(models.Model):
    nombre = models.CharField(max_length=200, verbose_name="Nombre")
    descripcion = models.TextField(verbose_name="Descripción")
    telefono = models.CharField(max_length=20, verbose_name="Teléfono")
    pais = models.CharField(max_length=100, verbose_name="País")
    correo = models.EmailField(verbose_name="Correo electrónico")
    direccion = models.TextField(verbose_name="Dirección")

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse("proveedores:detail", kwargs={"pk": self.pk})
