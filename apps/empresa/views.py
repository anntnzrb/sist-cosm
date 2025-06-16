from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView
from django.views import View
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Empresa
from .forms import EmpresaForm


class EmpresaView(View):
    def get(self, request):
        try:
            empresa = Empresa.objects.get()
            return render(request, 'empresa/detail.html', {'empresa': empresa})
        except Empresa.DoesNotExist:
            return render(request, 'empresa/no_info.html')


class EmpresaCreateView(CreateView):
    model = Empresa
    form_class = EmpresaForm
    template_name = 'empresa/create.html'
    success_url = reverse_lazy('empresa:detail')
    
    def get(self, request, *args, **kwargs):
        if Empresa.objects.exists():
            messages.warning(request, 'Ya existe información de la empresa. Puede editarla.')
            return redirect('empresa:detail')
        return super().get(request, *args, **kwargs)
    
    def form_valid(self, form):
        messages.success(self.request, 'Información de empresa creada exitosamente.')
        return super().form_valid(form)


class EmpresaUpdateView(UpdateView):
    model = Empresa
    form_class = EmpresaForm
    template_name = 'empresa/update.html'
    success_url = reverse_lazy('empresa:detail')
    
    def get_object(self):
        return Empresa.objects.get()
    
    def form_valid(self, form):
        messages.success(self.request, 'Información de empresa actualizada exitosamente.')
        return super().form_valid(form)
