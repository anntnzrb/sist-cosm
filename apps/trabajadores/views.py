from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import TrabajadorForm
from .models import Trabajador


class TrabajadorListView(ListView):
    model = Trabajador
    template_name = "trabajadores/list.html"
    context_object_name = "trabajadores"
    paginate_by = 8


class TrabajadorCreateView(CreateView):
    model = Trabajador
    form_class = TrabajadorForm
    template_name = "trabajadores/create.html"
    success_url = reverse_lazy("trabajadores:list")

    def form_valid(self, form):
        messages.success(self.request, "Trabajador creado exitosamente.")
        return super().form_valid(form)


class TrabajadorUpdateView(UpdateView):
    model = Trabajador
    form_class = TrabajadorForm
    template_name = "trabajadores/update.html"
    success_url = reverse_lazy("trabajadores:list")

    def form_valid(self, form):
        messages.success(self.request, "Trabajador actualizado exitosamente.")
        return super().form_valid(form)


class TrabajadorDeleteView(DeleteView):
    model = Trabajador
    template_name = "trabajadores/delete.html"
    success_url = reverse_lazy("trabajadores:list")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Trabajador eliminado exitosamente.")
        return super().delete(request, *args, **kwargs)
