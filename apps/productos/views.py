from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import ProductoForm
from .models import Producto


class ProductoListView(ListView):
    model = Producto
    template_name = "productos/list.html"
    context_object_name = "productos"
    paginate_by = 12


class ProductoCreateView(CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = "productos/create.html"
    success_url = reverse_lazy("productos:list")

    def form_valid(self, form):
        messages.success(self.request, "Producto creado exitosamente.")
        return super().form_valid(form)


class ProductoUpdateView(UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = "productos/update.html"
    success_url = reverse_lazy("productos:list")

    def form_valid(self, form):
        messages.success(self.request, "Producto actualizado exitosamente.")
        return super().form_valid(form)


class ProductoDeleteView(DeleteView):
    model = Producto
    template_name = "productos/delete.html"
    success_url = reverse_lazy("productos:list")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Producto eliminado exitosamente.")
        return super().delete(request, *args, **kwargs)
