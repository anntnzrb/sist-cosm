from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import ProveedorForm
from .models import Proveedor


class ProveedorListView(ListView):
    model = Proveedor
    template_name = "proveedores/list.html"
    context_object_name = "proveedores"
    paginate_by = 12


class ProveedorCreateView(CreateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = "proveedores/create.html"
    success_url = reverse_lazy("proveedores:list")

    def form_valid(self, form):
        messages.success(self.request, "Proveedor creado exitosamente.")
        return super().form_valid(form)


class ProveedorUpdateView(UpdateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = "proveedores/update.html"
    success_url = reverse_lazy("proveedores:list")

    def form_valid(self, form):
        messages.success(self.request, "Proveedor actualizado exitosamente.")
        return super().form_valid(form)


class ProveedorDeleteView(DeleteView):
    model = Proveedor
    template_name = "proveedores/delete.html"
    success_url = reverse_lazy("proveedores:list")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Proveedor eliminado exitosamente.")
        return super().delete(request, *args, **kwargs)
